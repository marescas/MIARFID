;Header and description

(define (domain puerto)

;remove requirements that are not needed
(:requirements :strips :typing :fluents :durative-actions )

(:types 
    grua
    contenedorObjetivo
    contenedor
    pila
    cinta
    muelle
    nivel
    -object
)

; un-comment following line if constants are needed
;(:constants )

(:predicates 
    ; un contenedor pila o grua esta en una pila o un muelle o una cinta o grua
    (en ?c - (either contenedor pila grua) ?p - (either pila muelle cinta grua) ) 
    (encima ?c1 - contenedor ?c2 - (either contenedor pila)  ) ; C1 está encima de c2
    (top ?c - (either contenedor pila) ?p - pila); c está en la cima de la pila p
    (libre ?x - (either grua cinta)); La grua está ocupada cargando un contenedor
    (conecta ?c - cinta ?m1 - muelle ?m2 - muelle); la cinta c conecta los muelles m1 y m2 en ese orden
    (next ?n1 - nivel ?n2 - nivel) ;siguiente nivel de n1 es n2 
    (altura ?p - pila ?n - nivel ); altura de la pila p
    (disponible ?c - (either contenedor pila) )
    (verde ?c - contenedor)
    (noverde ?c - (either contenedor pila))
    (inicioCinta ?c - contenedor ?t - cinta) ;cuando el contenedor este en la cinta pero no haya llegado a su destino
    (finalCinta ?c - contenedor ?t - cinta)  ;cuando el contendor haya llegado a su destino
    
)

(:functions 
    (peso ?c1 - contenedor)
    (conaltura ?a1 - nivel)
    (tiempoTransporte)
)

(:durative-action coger
    :parameters (?g - grua ?p - pila ?c1 - contenedor ?c2 -(either contenedor pila) ?m - muelle  ?nOrigen - nivel ?nDestino  - nivel )
    :duration (= ?duration (/ (peso ?c1) (conaltura ?nOrigen)))
    :condition (and
                     
                    (over all (en ?p ?m)) ; pila estar en muelle
                    (over all (en ?g ?m )) ; grua estar en muelle
                    (at start (libre ?g))  ; grua estar libre
                    (at start (top ?c1 ?p)) ; contenedor estar en la cima de la pila
                    (at start (encima ?c1 ?c2)) ; contenedor estar encima de c2 siendo este un contenedor, contenedorObjetivo o una pila
                    (at start (en ?c1 ?p)) ; contenedor estar en la pila
                    (at start (altura ?p ?nOrigen)) ;la altura de la pila es norigen
                    (at start (next ?nDestino ?nOrigen)) ; existe una altura menor
                    (at start (disponible ?c1))
                    

                )
    :effect (and
            (at end (en ?c1 ?g)) ; el contenedor esta en la grua
            (at end (disponible ?c2)) ; el contenedor c2 pasa a estar disponible ya que es el nuevo top
            (at end (altura ?p ?nDestino)) ; la altura se decrementa
            (at end (en ?c2 ?p))
            (at end (top ?c2 ?p)); cambiamos el nuevo top
            (at end (not (en ?c1 ?p))) ; el contenedor ya no esta en la pila
            (at end (not (top ?c1 ?p))) ; no esta en el top
            (at end (not (encima ?c1 ?c2))) ;el contenedor c1 ya no esta de c2
            (at end (not (libre ?g))) ;La grua ya no está libre
            ;(nolibre ?g)
            (at end (not (altura ?p ?nOrigen))) ; altura incorrecta eliminada
            (at end (not (disponible ?c1))) ; el contenedor en la grua no esta disponible
            
     )
)

(:durative-action dejarSobreNoVerde
    :parameters (?g - grua ?p - pila ?c1 -contenedor ?c2 - (either contenedor pila) ?m - muelle ?nOrigen -nivel ?nDestino  -nivel)
    :duration (= ?duration (/ (peso ?c1) (conaltura ?nDestino)))
    :condition (and
        (at start (en ?c1 ?g)) ; el contenedor debe estar en la grua
        (over all (en ?g ?m)) ; la grua debe estar en el muelle origen
        (over all (en ?p ?m)); la pila debe estar en el muelle
        (over all (en ?c2 ?p)); c2 debe estar en la pila
        (at start (top ?c2 ?p)); el contenedor 2 debe ser la cima de la pila
        (over all (noverde ?c2)) ; el contenedor en la pila no debe ser verde
        (at start (altura ?p ?nOrigen)) ;la altura de la pila es norigen
        (over all (next ?nOrigen ?nDestino)) ; existe una altura menor
     )
    :effect (and
        (at end (libre ?g)) ;la grua pasa a estar libre
        (at end (en ?c1 ?p)) ; el contenedor esta en la pila
        (at end (encima ?c1 ?c2)) ; c1 esta encima de c2
        (at end (top ?c1 ?p)) ; c1 pasa a ser el top de la pila p
        (at end (disponible ?c1)) ; c1 pasa a estar disponible
        (at end (altura ?p ?nDestino)) ; la altura se decrementa
        (at end (not (en ?c1 ?g))) ; el contenedor no esta en la grua
        (at end (not (top ?c2 ?p))) ;c2 ya no es la cima de la pila
        (at end (not (disponible ?c2))) ; c2 ya no esta disponible
        (at end (not (altura ?p ?nOrigen))) ; altura incorrecta eliminada
        
     )
)

(:durative-action dejarBlancoSobreVerde
    :parameters (?g - grua ?p - pila ?c1 - contenedor ?c2 - contenedor ?m - muelle ?nOrigen - nivel ?nDestino  - nivel)
    :duration (= ?duration (/ (peso ?c1) (conaltura ?nDestino)))
    :condition (and
        (at start (en ?c1 ?g)) ; el contenedor debe estar en la grua
        (over all (en ?g ?m)) ; la grua debe estar en el muelle origen
        (over all (en ?p ?m)) ; la pila debe estar en el muelle
        (over all (en ?c2 ?p)) ; c2 debe estar en la pila
        (at start (top ?c2 ?p)) ; el contenedor 2 debe ser la cima de la pila
        (over all (verde ?c2)) ; el contenedor en la pila no debe ser verde
        (at start (altura ?p ?nOrigen)) ;la altura de la pila es norigen
        (over all (next ?nOrigen ?nDestino)) ; existe una altura menor
        (over all (noverde ?c1)) ; c1 no debe ser verde
     )
    :effect (and
        (at end (libre ?g)) ;la grua pasa a estar libre
        (at end (en ?c1 ?p)) ; el contenedor esta en la la cinta
        (at end(encima ?c1 ?c2)) ; c1 esta encima de c2
        (at end (top ?c1 ?p)) ; c1 pasa a ser el top de la pila p
        (at end (disponible ?c1)) ; c1 pasa a estar disponible
        (at end (altura ?p ?nDestino)) ; la altura se decrementa
        ;(not (nolibre ?g)) ; la grua pasa a estar libre
        (at end (not (en ?c1 ?g))) ; el contenedor no esta en la grua
        (at end (not (top ?c2 ?p))) ;c2 ya no es la cima de la pila
        (at end (not (disponible ?c2))) ; c2 ya no esta disponible
        (at end (not (altura ?p ?nOrigen))) ; altura incorrecta eliminada  
     )
)

(:durative-action dejarVerdeSobreVerde
    :parameters (?g - grua ?p - pila ?c1 -contenedor ?c2 - contenedor ?m - muelle ?nOrigen -nivel ?nDestino  -nivel)
    :duration (= ?duration (/ (peso ?c1) (conaltura ?nDestino)))
    :condition (and
        (at start (en ?c1 ?g)) ; el contenedor debe estar en la grua
        (over all (en ?g ?m)) ; la grua debe estar en el muelle origen
        (over all (en ?p ?m)); la pila debe estar en el muelle
        (over all (en ?c2 ?p)); c2 debe estar en la pila
        (at start (top ?c2 ?p)); el contenedor 2 debe ser la cima de la pila
        (over all (verde ?c2)) ; el contenedor en la pila  debe ser verde
        (at start (altura ?p ?nOrigen)) ;la altura de la pila es norigen
        (over all (next ?nOrigen ?nDestino)) ; existe una altura menor
        (over all (verde ?c1)) ;c1 debe ser verde
     )
    :effect (and
        (at end (libre ?g)) ;la grua pasa a estar libre
        (at end (en ?c1 ?p)) ; el contenedor esta en la la pila
        (at end (encima ?c1 ?c2)) ; c1 esta encima de c2
        (at end (top ?c1 ?p)) ; c1 pasa a ser el top de la pila p
        (at end (disponible ?c1)) ; c1 pasa a estar disponible
        (at end (altura ?p ?nDestino)) ; la altura se decrementa
        (at end (not (en ?c1 ?g))) ; el contenedor no esta en la grua
        (at end (not (top ?c2 ?p))) ;c2 ya no es la cima de la pila
        ;(not (disponible ?c2)) ; c2 ya no esta disponible
        (at end (not (altura ?p ?nOrigen))) ; altura incorrecta eliminada
        
     )
)

(:durative-action mover
    :parameters (?c - contenedor ?mOrigen - muelle ?mDestino - muelle ?t - cinta)
    :duration (= ?duration (tiempoTransporte))
    :condition (and
        (at start (inicioCinta ?c ?t)) ; solo al comienzo debe comprobarse que el contenedor se encuentra al inicio de la cinta 
        (over all (en ?c ?t)) ; el contenedor debe estar en la cinta durante todo el trayecto
        (over all (conecta ?t ?mOrigen ?mDestino)) ; en todo momento se debe comprobar la conexion entre muelles
     )
    :effect (and 
        (at end (finalCinta ?c ?t)) ; al final de la accion el contenedor estara al final de la cinta
        (at end (not (inicioCinta ?c ?t))) ; al final no puede estar al principio de la cinta
    )
)

(:durative-action cogerDeCinta
    :parameters (?c - contenedor ?g - grua ?mOrigen - muelle ?mDestino - muelle ?t - cinta)
    :duration (= ?duration (peso ?c))
    :condition (and
        (at start (en ?c ?t)) ; el contenedor debe estar en la cinta 
        (at start (finalCinta ?c ?t)) ;solo se puede recoger si se encuentra al final de la cinta, es decir accesible a la grua que coge
        (over all (en ?g ?mDestino)) ; la grua debe estar en el muelle destino
        (over all (conecta ?t ?mOrigen ?mDestino )); debe existir una conexion entre el muelle origen y el muelle destino
        (at start (libre ?g)) ; TODO DUDA la grua no tiene pq estar libre hasta que el contenedor haya llegado al extremo de la cinta?????????
     )
    :effect (and 
        (at end (not (libre ?g))) ;la grua ya no estar libre
        (at end (en ?c ?g)) ; el contenedor esta en la la grua
        (at end (not (en ?c ?t))) ; el contenedor no esta en la cinta
        (at end (not (finalCinta ?c ?t))) ;si no esta en la cinta no esta al final de esta
        (at end (libre ?t)) ; la cinta esta ocupada 
        (at end (en ?c ?mDestino)) ;el contenedor ya tiene ubicacion
    )
)

(:durative-action dejarEnCinta
    :parameters (?c -contenedor ?g - grua ?mOrigen - muelle ?mDestino - muelle ?t - cinta)
    :duration (= ?duration (peso ?c))
    :condition (and
        (at start (en ?c ?g)) ; el contenedor debe estar en la grua
        (over all (en ?g ?mOrigen)) ; la grua debe estar en el muelle origen
        (over all (conecta ?t ?mOrigen ?mDestino)) ; debe existir una conexion entre el muelle origen y el muelle destino
        (at end (libre ?t)) ; la cinta debe estar libre al final, pq aqui no se contempla el tiempo de transporte
        (at start (en ?c ?mOrigen)) ;el contenedor esta en el muelle origen
     )
    :effect (and 
        (at end (libre ?g)) ;la grua pasa a estar libre
        (at end (en ?c ?t)) ; el contenedor esta en la la cinta
        (at end (inicioCinta ?c ?t)) ;el contendor se encuentra al inicio de la cinta
        (at end (not (en ?c ?g))) ; el contenedor no esta en la grua
        (at end (not (libre ?t))) ; la cinta esta ocupada
        (at end (not (en ?c ?mOrigen))) ;esta en la frontera "andorra"
    )
)

)



