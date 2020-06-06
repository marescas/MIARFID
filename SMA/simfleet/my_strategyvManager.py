"""
author: Marcos Esteve Casademunt y David Gimeno Gomez

En esta estrategia el manager recibe las posiciones de todos los transportes de forma que cuando llega un cliente
 organiza y se envia un mensaje a todos los transportes en orden por distancia.
Además se intenta dar mayor prioridad a aquellos transportes que estan mas cerca del cliente y además sean trayectos cortos
es decir, minimizar distancia(posicion_transporte,origen_cliente)+distancia(origen_cliente,destino_cliente)
"""

import json
import random

from loguru import logger
from simfleet.helpers import PathRequestException, distance_in_meters
from simfleet.protocol import REQUEST_PERFORMATIVE, ACCEPT_PERFORMATIVE, REFUSE_PERFORMATIVE, PROPOSE_PERFORMATIVE, \
    CANCEL_PERFORMATIVE, INFORM_PERFORMATIVE, QUERY_PROTOCOL, REQUEST_PROTOCOL
from simfleet.utils import TRANSPORT_WAITING, TRANSPORT_WAITING_FOR_APPROVAL, CUSTOMER_WAITING, TRANSPORT_MOVING_TO_CUSTOMER, \
    CUSTOMER_ASSIGNED, TRANSPORT_WAITING_FOR_STATION_APPROVAL, TRANSPORT_MOVING_TO_STATION, \
    TRANSPORT_CHARGING, TRANSPORT_CHARGED, TRANSPORT_NEEDS_CHARGING

from simfleet.fleetmanager import FleetManagerStrategyBehaviour
from simfleet.customer import CustomerStrategyBehaviour
from simfleet.transport import TransportStrategyBehaviour


################################################################
#                                                              #
#                     FleetManager Strategy                    #
#                                                              #
################################################################
from spade.message import MessageBase, Message


class MyFleetManagerStrategy(FleetManagerStrategyBehaviour):
    """
    Cuando le llega una petición del cliente la reenvia a todos los conductores por orden de cercania


    """
    async def on_start(self):
        #MODIFICADO
        await super().on_start()
        self.set("transportPosition",{})


    async def run(self):
        if not self.agent.registration:
            await self.send_registration()

        msg = await self.receive(timeout=5)
        logger.info("Manager received message: {}".format(msg))
        jidsTransport = [str(transport["jid"]) for transport in self.get_transport_agents().values()]
        if str(msg.sender) in jidsTransport :
            #Si es un transporte me guardo la posicion actual del transporte
            positionDict =json.loads(msg.body)
            print("mensaje de transporte recibido")
            transportPosition = self.get("transportPosition")
            transportPosition[str(msg.sender)] = positionDict["position"]
            self.set("transportPosition",transportPosition)
        elif str(msg.sender) not in jidsTransport:
            #si es un cliente organizo los transportes con la metrica propuesta y enviaremos un mensaje a todos ordenados por cercania
            transportPosition = self.get("transportPosition")
            posicion_cliente = json.loads(msg.body)["origin"]
            destino_cliente = json.loads(msg.body)["dest"]
            logger.info("posicion del cliente: "+str(posicion_cliente))
            transportsWithDistances = [(transport["jid"],distance_in_meters(posicion_cliente,destino_cliente)+distance_in_meters(posicion_cliente,transportPosition[transport["jid"]])) for transport in self.get_transport_agents().values()]
            transportsWithDistances = sorted(transportsWithDistances,key= lambda x:x[1])

            logger.info("transporteXDistancia"+str(transportsWithDistances))
            for transport in transportsWithDistances:
                msg.to = str(transport[0])
                logger.debug("Manager sent request to transport {}".format(transport[0]))
                await self.send(msg)

                



################################################################
#                                                              #
#                     Transport Strategy                       #
#                                                              #
################################################################
class MyTransportStrategy(TransportStrategyBehaviour):
    """
    The default strategy for the Transport agent. By default it accepts every request it receives if available.
    """
    async def on_start(self):
        #Envio mi posicion al manager
        await super().on_start()
        msg = Message()
        msg.to = self.agent.fleetmanager_id
        msg.set_metadata("protocol", REQUEST_PROTOCOL)
        msg.set_metadata("performative", REQUEST_PERFORMATIVE)
        msg.body = json.dumps({"position":self.agent.get_position()})
        await self.send(msg)
        logger.info("msg al manager con mi posicion"+str(msg))

    async def run(self):
        #Actualizamos la posición que tiene de mi el manager
        if self.agent.status != TRANSPORT_MOVING_TO_CUSTOMER:
            msg = Message()
            msg.to = self.agent.fleetmanager_id
            msg.set_metadata("protocol", REQUEST_PROTOCOL)
            msg.set_metadata("performative", REQUEST_PERFORMATIVE)
            msg.body = json.dumps({"position": self.agent.get_position()})
            await self.send(msg)
            logger.info("msg al manager con mi posicion" + str(msg))

        await self.send(msg)
        if self.agent.needs_charging():
            if self.agent.stations is None or len(self.agent.stations) < 1:
                logger.warning("Transport {} looking for a station.".format(self.agent.name))
                await self.send_get_stations()
            else:
                station = random.choice(list(self.agent.stations.keys()))
                logger.info("Transport {} reserving station {}.".format(self.agent.name, station))
                await self.send_proposal(station)
                self.agent.status = TRANSPORT_WAITING_FOR_STATION_APPROVAL

        msg = await self.receive(timeout=5)
        if not msg:
            return
        logger.debug("Transport received message: {}".format(msg))
        try:
            content = json.loads(msg.body)
        except TypeError:
            content = {}

        performative = msg.get_metadata("performative")
        protocol = msg.get_metadata("protocol")

        if protocol == QUERY_PROTOCOL:
            if performative == INFORM_PERFORMATIVE:
                self.agent.stations = content
                logger.info("Got list of current stations: {}".format(list(self.agent.stations.keys())))
            elif performative == CANCEL_PERFORMATIVE:
                logger.info("Cancellation of request for stations information.")

        elif protocol == REQUEST_PROTOCOL:
            logger.debug("Transport {} received request protocol from customer/station.".format(self.agent.name))

            if performative == REQUEST_PERFORMATIVE:
                if self.agent.status == TRANSPORT_WAITING:
                    if not self.has_enough_autonomy(content["origin"], content["dest"]):
                        await self.cancel_proposal(content["customer_id"])
                        self.agent.status = TRANSPORT_NEEDS_CHARGING
                    else:
                        await self.send_proposal(content["customer_id"], {})
                        self.agent.status = TRANSPORT_WAITING_FOR_APPROVAL

            elif performative == ACCEPT_PERFORMATIVE:
                if self.agent.status == TRANSPORT_WAITING_FOR_APPROVAL:
                    logger.debug("Transport {} got accept from {}".format(self.agent.name,
                                                                          content["customer_id"]))
                    try:
                        self.agent.status = TRANSPORT_MOVING_TO_CUSTOMER
                        await self.pick_up_customer(content["customer_id"], content["origin"], content["dest"])
                    except PathRequestException:
                        logger.error("Transport {} could not get a path to customer {}. Cancelling..."
                                     .format(self.agent.name, content["customer_id"]))
                        self.agent.status = TRANSPORT_WAITING
                        await self.cancel_proposal(content["customer_id"])
                    except Exception as e:
                        logger.error("Unexpected error in transport {}: {}".format(self.agent.name, e))
                        await self.cancel_proposal(content["customer_id"])
                        self.agent.status = TRANSPORT_WAITING
                else:
                    await self.cancel_proposal(content["customer_id"])

            elif performative == REFUSE_PERFORMATIVE:
                logger.debug("Transport {} got refusal from customer/station".format(self.agent.name))
                self.agent.status = TRANSPORT_WAITING

            elif performative == INFORM_PERFORMATIVE:
                if self.agent.status == TRANSPORT_WAITING_FOR_STATION_APPROVAL:
                    logger.info("Transport {} got accept from station {}".format(self.agent.name,
                                                                                 content["station_id"]))
                    try:
                        self.agent.status = TRANSPORT_MOVING_TO_STATION
                        await self.send_confirmation_travel(content["station_id"])
                        await self.go_to_the_station(content["station_id"], content["dest"])
                    except PathRequestException:
                        logger.error("Transport {} could not get a path to station {}. Cancelling..."
                                     .format(self.agent.name, content["station_id"]))
                        self.agent.status = TRANSPORT_WAITING
                        await self.cancel_proposal(content["station_id"])
                    except Exception as e:
                        logger.error("Unexpected error in transport {}: {}".format(self.agent.name, e))
                        await self.cancel_proposal(content["station_id"])
                        self.agent.status = TRANSPORT_WAITING
                elif self.agent.status == TRANSPORT_CHARGING:
                    if content["status"] == TRANSPORT_CHARGED:
                        self.agent.transport_charged()
                        await self.agent.drop_station()

            elif performative == CANCEL_PERFORMATIVE:
                logger.info("Cancellation of request for {} information".format(self.agent.fleet_type))


################################################################
#                                                              #
#                       Customer Strategy                      #
#                                                              #
################################################################
class MyCustomerStrategy(CustomerStrategyBehaviour):
    """
    The default strategy for the Customer agent. By default it accepts the first proposal it receives.
    """

    async def run(self):
        if self.agent.fleetmanagers is None:
            await self.send_get_managers(self.agent.fleet_type)

            msg = await self.receive(timeout=5)
            if msg:
                performative = msg.get_metadata("performative")
                if performative == INFORM_PERFORMATIVE:
                    self.agent.fleetmanagers = json.loads(msg.body)
                    return
                elif performative == CANCEL_PERFORMATIVE:
                    logger.info("Cancellation of request for {} information".format(self.agent.type_service))
                    return

        if self.agent.status == CUSTOMER_WAITING:
            #Necesito un transporte
            await self.send_request()

        msg = await self.receive(timeout=5)

        if msg:
            performative = msg.get_metadata("performative")
            transport_id = msg.sender
            if performative == PROPOSE_PERFORMATIVE:
                if self.agent.status == CUSTOMER_WAITING:
                    logger.debug(
                        "Customer {} received proposal from transport {}".format(self.agent.name, transport_id))
                    await self.accept_transport(transport_id)
                    self.agent.status = CUSTOMER_ASSIGNED
                else:
                    await self.refuse_transport(transport_id)

            elif performative == CANCEL_PERFORMATIVE:
                if self.agent.transport_assigned == str(transport_id):
                    logger.warning(
                        "Customer {} received a CANCEL from Transport {}.".format(self.agent.name, transport_id))
                    self.agent.status = CUSTOMER_WAITING

