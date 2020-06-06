import json
import random
import asyncio
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
class MyFleetManagerStrategy(FleetManagerStrategyBehaviour):
    """
    The default strategy for the FleetManager agent. By default it delegates all requests to all transports.
    """

    async def run(self):
        if not self.agent.registration:
            await self.send_registration()

        msg = await self.receive(timeout=5)
        logger.debug("Manager received message: {}".format(msg))
        if msg:
            for transport in self.get_transport_agents().values():
                msg.to = str(transport["jid"])
                logger.debug("Manager sent request to transport {}".format(transport["name"]))
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

    async def run(self):
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
                    #si el transpotrte no esta ocupado
                    if not self.has_enough_autonomy(content["origin"], content["dest"]):
                        await self.cancel_proposal(content["customer_id"])
                        self.agent.status = TRANSPORT_NEEDS_CHARGING
                    else:
                        #si tenemos gasolina
                        await self.send_proposal(content["customer_id"], {"position":self.agent.get_position()})
                        logger.info("client %s position %s " %(content["customer_id"],self.agent.get_position()))
                        self.agent.status = TRANSPORT_WAITING_FOR_APPROVAL

            elif performative == ACCEPT_PERFORMATIVE:
                #cliente nos contesta
                if self.agent.status == TRANSPORT_WAITING_FOR_APPROVAL:
                    #si no nos lo han quitado
                    logger.debug("Transport {} got accept from {}".format(self.agent.name,
                                                                          content["customer_id"]))
                    try:
                        self.agent.status = TRANSPORT_MOVING_TO_CUSTOMER #voy a por el cliente
                        await self.pick_up_customer(content["customer_id"], content["origin"], content["dest"]) #acción de ir a por el cliente
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
                    #si ya esta ocupado
                    await self.cancel_proposal(content["customer_id"])

            elif performative == REFUSE_PERFORMATIVE:
                logger.debug("Transport {} got refusal from customer/station".format(self.agent.name))
                self.agent.status = TRANSPORT_WAITING
                await self.send_proposal(content["customer_id"], {"position": self.agent.get_position()})


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
    async def on_start(self):
        await super().on_start()
        self.agent.set("misOportunidades",[])
        print("hola")
    async def run(self):
        if self.agent.fleetmanagers is None:
            #pido la direccion de los managers si no la conozco
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
            await self.send_request(content={})

        msg = await self.receive(timeout=5)

        if msg:
            performative = msg.get_metadata("performative")
            transport_id = msg.sender
            if performative == PROPOSE_PERFORMATIVE:
                if self.agent.status == CUSTOMER_WAITING:
                    #soy cliente esperando

                    posicionTransporte = json.loads(msg.body)["position"]

                    logger.info("Trozo de mierda"  +str(posicionTransporte))
                    listaPos = self.agent.get("misOportunidades")
                    distance=  distance_in_meters(self.agent.get_position(),posicionTransporte)
                    logger.info("distancia trozo de mierda"+str(distance))
                    listaPos.append((str(transport_id),distance))
                    self.agent.set("misOportunidades",listaPos)

                    print(self.agent.get("misOportunidades"))
                    #await asyncio.sleep(3)
                    if len(self.agent.get("misOportunidades")) > 1:
                        sortListPosiciones = sorted(self.agent.get("misOportunidades"),key= lambda x:x[1])
                        print("lista ordenada", sortListPosiciones,len(sortListPosiciones))
                        elegido = sortListPosiciones.pop(0)
                        print("lista ordenada", sortListPosiciones,len(sortListPosiciones))
                        self.agent.set("misOportunidades", sortListPosiciones)
                        logger.debug(
                            "Customer {} received proposal from transport {}".format(self.agent.name, elegido[0]))
                        await self.accept_transport(elegido[0])
                        self.agent.status = CUSTOMER_ASSIGNED
                        #for noelegido in sortListPosiciones:
                        #    await self.refuse_transport(noelegido[0])


                    #logger.info("posicion"+str(posicionTransporte))


                    #if len(sortListPosiciones)>1:


                else:
                    for noelegido in self.agent.get("misOportunidades"):
                        await self.refuse_transport(transport_id)

            elif performative == CANCEL_PERFORMATIVE:
                if self.agent.transport_assigned == str(transport_id):
                    logger.warning(
                        "Customer {} received a CANCEL from Transport {}.".format(self.agent.name, transport_id))
                    self.agent.status = CUSTOMER_WAITING
                    misTaxis = self.agent.get("misOportunidades")
                    elegido = misTaxis.pop(0)
                    print("lista ordenada", misTaxis, len(misTaxis))
                    self.agent.set("misOportunidades", misTaxis)
                    logger.debug(
                        "Customer {} received proposal from transport {}".format(self.agent.name, elegido[0]))
                    await self.accept_transport(elegido[0])
                    self.agent.status = CUSTOMER_ASSIGNED
                    for noelegido in misTaxis:
                        await self.refuse_transport(noelegido[0])

