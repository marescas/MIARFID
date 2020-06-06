;Header and description

(define (domain puerto)

;remove requirements that are not needed
(:requirements :strips :typing )

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
    (nolibre ?t - (either grua cinta))
    (nodisponible ?c -(either contenedor pila))
)


;(:functions ;todo: define numeric functions here
;)

;define actions here
;muelle podemos quitarlo??
(:action coger
    :parameters (?g - grua ?p - pila ?c1 - contenedor ?c2 -(either contenedor pila) ?m - muelle  ?nOrigen - nivel ?nDestino  - nivel )
    :precondition (and 
                    (en ?p ?m) ; pila estar en muelle
                    (en ?g ?m ) ; grua estar en muelle
                    (libre ?g)  ; grua estar libre
                    (top ?c1 ?p) ; contenedor estar en la cima de la pila
                    (encima ?c1 ?c2) ; contenedor estar encima de c2 siendo este un contenedor, contenedorObjetivo o una pila
                    (en ?c1 ?p); contenedor estar en la pila
                    (altura ?p ?nOrigen) ;la altura de la pila es norigen
                    (next ?nDestino ?nOrigen) ; existe una altura menor
                    ;(disponible ?c1)

                )
    :effect (and
            (en ?c1 ?g) ; el contenedor esta en la grua
            ;(disponible ?c2) ; el contenedor c2 pasa a estar disponible ya que es el nuevo top
            (altura ?p ?nDestino) ; la altura se decrementa
            (en ?c2 ?p)
            (top ?c2 ?p); cambiamos el nuevo top
            (not (en ?c1 ?p)) ; el contenedor ya no esta en la pila
            (not (top ?c1 ?p)); no esta en el top
            (not (encima ?c1 ?c2)) ;el contenedor c1 ya no esta de c2
            (not (libre ?g)) ;La grua ya no está libre
            (nolibre ?g)
            (not (altura ?p ?nOrigen)) ; altura incorrecta eliminada
            ;(not (disponible ?c1)) ; el contenedor en la grua no esta disponible
            
     )
)


(:action dejarEnCinta
    :parameters (?c -contenedor ?g - grua ?mOrigen - muelle ?mDestino - muelle ?t - cinta)
    :precondition (and
        (en ?c ?g) ; el contenedor debe estar en la grua
        (nolibre ?g) ;grua no libre
        (en ?g ?mOrigen) ; la grua debe estar en el muelle origen
        (conecta ?t ?mOrigen ?mDestino ); debe existir una conexion entre el muelle origen y el muelle destino
        (libre ?t) ; la cinta debe estar libre
        (en ?c ?mOrigen) ;el contenedor esta en el muelle origen
     )
    :effect (and 
        (libre ?g) ;la grua pasa a estar libre
        (en ?c ?t) ; el contenedor esta en la la cinta
        (nolibre ?t)
        (not (en ?c ?g)) ; el contenedor no esta en la grua
        (not (libre ?t)) ; la cinta esta ocupada
        (not (nolibre ?g)) 
        (not (en ?c ?mOrigen)) ;esta en la frontera "andorra"
    )
)
(:action dejarSobreNoVerde
    :parameters (?c1 -contenedor ?c2 - (either contenedor pila) ?g - grua ?m - muelle ?p - pila ?nOrigen -nivel ?nDestino  -nivel)
    :precondition (and
        (en ?c1 ?g) ; el contenedor debe estar en la grua
        (nolibre ?g) ;grua no libre
        (en ?g ?m) ; la grua debe estar en el muelle origen
        (en ?p ?m); la pila debe estar en el muelle
        (en ?c2 ?p); c2 debe estar en la pila
        (top ?c2 ?p); el contenedor 2 debe ser la cima de la pila
        (noverde ?c2) ; el contenedor en la pila no debe ser verde
        (altura ?p ?nOrigen) ;la altura de la pila es norigen
        (next ?nOrigen ?nDestino) ; existe una altura menor
     )
    :effect (and
        (libre ?g) ;la grua pasa a estar libre
        (en ?c1 ?p) ; el contenedor esta en la la cinta
        (encima ?c1 ?c2) ; c1 esta encima de c2
        (top ?c1 ?p) ; c1 pasa a ser el top de la pila p
        (disponible ?c1) ; c1 pasa a estar disponible
        (altura ?p ?nDestino) ; la altura se decrementa
        (not (nolibre ?g)) ; la grua pasa a estar libre
        (not (en ?c1 ?g)) ; el contenedor no esta en la grua
        (not (top ?c2 ?p)) ;c2 ya no es la cima de la pila
        (not (disponible ?c2)) ; c2 ya no esta disponible
        (not (altura ?p ?nOrigen)) ; altura incorrecta eliminada
        
     )
)

(:action dejarVerde
    :parameters (?c1 - contenedor ?c2 - contenedor ?g - grua ?m - muelle ?p - pila ?nOrigen - nivel ?nDestino  - nivel)
    :precondition (and
        (en ?c1 ?g) ; el contenedor debe estar en la grua
        (nolibre ?g) ;grua no libre
        (en ?g ?m) ; la grua debe estar en el muelle origen
        (en ?p ?m); la pila debe estar en el muelle
        (en ?c2 ?p); c2 debe estar en la pila
        (top ?c2 ?p); el contenedor 2 debe ser la cima de la pila
        ;(verde ?c2) ; el contenedor en la pila  debe ser verde
        (altura ?p ?nOrigen) ;la altura de la pila es norigen
        (next ?nOrigen ?nDestino) ; existe una altura menor
        (verde ?c1) ;c1 debe ser verde
     )
    :effect (and 
        (libre ?g) ;la grua pasa a estar libre
        (en ?c1 ?p) ; el contenedor esta en la la cinta
        (encima ?c1 ?c2) ; c1 esta encima de c2
        (top ?c1 ?p) ; c1 pasa a ser el top de la pila p
        ;(disponible ?c1) ; c1 pasa a estar disponible ¿PORQUE HABRIA QUE VER SI ESTA EN EL MUELLE DESTINO NO?
        (altura ?p ?nDestino) ; la altura se decrementa
        (not (nolibre ?g)) ; la grua pasa a estar libre
        (not (en ?c1 ?g)) ; el contenedor no esta en la grua
        (not (top ?c2 ?p)) ;c2 ya no es la cima de la pila
        ;(not (disponible ?c2)) ; c2 ya no esta disponible
        (not (altura ?p ?nOrigen)) ; altura incorrecta eliminada
    )
)









(:action dejarBlancoSobreVerde
    :parameters (?c1 - contenedor ?c2 - contenedor ?g - grua ?m - muelle ?p - pila ?nOrigen - nivel ?nDestino  - nivel)
    :precondition (and
        (en ?c1 ?g) ; el contenedor debe estar en la grua
        (nolibre ?g) ;grua no libre
        (en ?g ?m) ; la grua debe estar en el muelle origen
        (en ?p ?m); la pila debe estar en el muelle
        (en ?c2 ?p); c2 debe estar en la pila
        (top ?c2 ?p); el contenedor 2 debe ser la cima de la pila
        (verde ?c2) ; el contenedor en la pila no debe ser verde
        (altura ?p ?nOrigen) ;la altura de la pila es norigen
        (next ?nOrigen ?nDestino) ; existe una altura menor
        (noverde ?c1) ; c1 no debe ser verde
     )
    :effect (and
        (libre ?g) ;la grua pasa a estar libre
        (en ?c1 ?p) ; el contenedor esta en la la cinta
        (encima ?c1 ?c2) ; c1 esta encima de c2
        (top ?c1 ?p) ; c1 pasa a ser el top de la pila p
        (disponible ?c1) ; c1 pasa a estar disponible
        (altura ?p ?nDestino) ; la altura se decrementa
        (not (nolibre ?g)) ; la grua pasa a estar libre
        (not (en ?c1 ?g)) ; el contenedor no esta en la grua
        (not (top ?c2 ?p)) ;c2 ya no es la cima de la pila
        (not (disponible ?c2)) ; c2 ya no esta disponible
        (not (altura ?p ?nOrigen)) ; altura incorrecta eliminada
        
     )
)

(:action dejarVerdeSobreVerde
    :parameters (?c1 -contenedor ?c2 - contenedor ?g - grua ?m - muelle ?p - pila ?nOrigen -nivel ?nDestino  -nivel)
    :precondition (and
        (en ?c1 ?g) ; el contenedor debe estar en la grua
        (nolibre ?g) ;grua no libre
        (en ?g ?m) ; la grua debe estar en el muelle origen
        (en ?p ?m); la pila debe estar en el muelle
        (en ?c2 ?p); c2 debe estar en la pila
        (top ?c2 ?p); el contenedor 2 debe ser la cima de la pila
        (verde ?c2) ; el contenedor en la pila  debe ser verde
        (altura ?p ?nOrigen) ;la altura de la pila es norigen
        (next ?nOrigen ?nDestino) ; existe una altura menor
        (verde ?c1) ;c1 debe ser verde
     )
    :effect (and
        (libre ?g) ;la grua pasa a estar libre
        (en ?c1 ?p) ; el contenedor esta en la la cinta
        (encima ?c1 ?c2) ; c1 esta encima de c2
        (top ?c1 ?p) ; c1 pasa a ser el top de la pila p
        (disponible ?c1) ; c1 pasa a estar disponible
        (altura ?p ?nDestino) ; la altura se decrementa
        (not (nolibre ?g)) ; la grua pasa a estar libre
        (not (en ?c1 ?g)) ; el contenedor no esta en la grua
        (not (top ?c2 ?p)) ;c2 ya no es la cima de la pila
        ;(not (disponible ?c2)) ; c2 ya no esta disponible
        (not (altura ?p ?nOrigen)) ; altura incorrecta eliminada
        
     )
)

(:action cogerDeCinta
    :parameters (?c - contenedor ?g - grua ?mOrigen - muelle ?mDestino - muelle ?t - cinta)
    :precondition (and
        (en ?c ?t) ; el contenedor debe estar en la cinta
        ;(not(libre ?t)) ;cinta no libre
        (nolibre ?t)
        (en ?g ?mDestino) ; la grua debe estar en el muelle destino
        (conecta ?t ?mOrigen ?mDestino ); debe existir una conexion entre el muelle origen y el muelle destino
        (libre ?g) ; la grua debe estar libre
     )
    :effect (and 
        (not(libre ?g)) ;la grua ya no estar libre
        (nolibre ?g)
        (en ?c ?g) ; el contenedor esta en la la grua
        (not (en ?c ?t)) ; el contenedor no esta en la cinta
        (libre ?t) ; la cinta esta ocupada 
        (en ?c ?mDestino) ;el contenedor ya tiene ubicacion
        (not (nolibre ?t)) ; PUEDE SER ESTO??
    )
)

)



