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
    ; un contenedor / contenedor objetivo / pila o grua esta en una pila o un muelle o una cinta o grua
    (en ?c - (either contenedor contenedorObjetivo pila grua) ?p - (either pila muelle cinta grua) ) 
    (encima ?c1 - (either contenedor contenedorObjetivo) ?c2 - (either contenedor contenedorObjetivo pila)  ) ; C1 está encima de c2
    (top ?c - (either contenedor contenedorObjetivo pila) ?p - pila); c está en la cima de la pila p
    (libre ?x - (either grua cinta)); La grua está ocupada cargando un contenedor
    (conecta ?c - cinta ?m1 - muelle ?m2 - muelle); la cinta c conecta los muelles m1 y m2 en ese orden
    (next ?n1 - nivel ?n2 - nivel) ;siguiente nivel de n1 es n2 
    (altura ?p - pila ?n - nivel ); altura de la pila p
    (disponible ?c - (either contenedor contenedorObjetivo))
)


;(:functions ;todo: define numeric functions here
;)

;define actions here
;muelle podemos quitarlo??
(:action coger
    :parameters (?g - grua ?p - pila ?c1- contenedor ?c2 -(either contenedor contenedorObjetivo pila) ?m - muelle  ?nOrigen -nivel ?nDestino  -nivel )
    :precondition (and 
                    (en ?p ?m) ; pila estar en muelle
                    (en ?g ?m ) ; grua estar en muelle
                    (libre ?g)  ; grua estar libre
                    (top ?c1 ?p) ; contenedor estar en la cima de la pila
                    (encima ?c1 ?c2) ; contenedor estar encima de c2 siendo este un contenedor, contenedorObjetivo o una pila
                    (en ?c ?p); contenedor estar en la pila
                    (altura ?p ?nOrigen) ;la altura de la pila es norigen
                    (next ?nDestino ?nOrigen) ; existe una altura menor
                    (disponible ?c1)

                )
    :effect (and
            (en ?c1 ?g) ; el contenedor esta en la grua
            (disponible ?c2) ; el contenedor c2 pasa a estar disponible ya que es el nuevo top
            (altura ?p ?nDestino) ; la altura se decrementa
            (top ?c2 ?p); cambiamos el nuevo top
            (not (en ?c1 ?p)) ; el contenedor ya no esta en la pila
            (not (top ?c1 ?p)); no esta en el top
            (not ((encima ?c1 ?c2))) ;el contenedor c1 ya no esta de c2
            (not (libre ?g)) ;La grua ya no está libre
            (not ((altura ?p ?nOrigen))) ; altura incorrecta eliminada
            (not (disponible ?c1)) ; el contenedor en la grua no esta disponible
            
     )
)
(:action dejarEnCinta
    :parameters (?c -(either contenedor contenedorObjetivo) ?g - grua ?mOrigen - muelle ?mDestino - muelle ?t - cinta)
    :precondition (and
        (en ?c ?g) ; el contenedor debe estar en la grua
        (not(libre ?g)) ;grua no libre
        (en ?g ?mOrigen) ; la grua debe estar en el muelle origen
        (conecta ?t ?mOrigen ?mDestino ); debe existir una conexion entre el muelle origen y el muelle destino
        (libre ?t) ; la cinta debe estar libre
        (en ?c ?mOrigen) ;el contenedor esta en el muelle origen
     )
    :effect (and 
        (libre ?g) ;la grua pasa a estar libre
        (en ?c ?t) ; el contenedor esta en la la cinta
        (not (en ?c ?g)) ; el contenedor no esta en la grua
        (not (libre ?t)) ; la cinta esta ocupada 
        (not (en ?c ?mOrigen)) ;esta en la frontera "andorra"
    )
)


(:action cogerDeCinta
    :parameters (?c -(either contenedor contenedorObjetivo) ?g - grua ?mOrigen - muelle ?mDestino - muelle ?t - cinta)
    :precondition (and
        (en ?c ?t) ; el contenedor debe estar en la cinta
        (not(libre ?t)) ;cinta no libre
        (en ?g ?mDestino) ; la grua debe estar en el muelle destino
        (conecta ?t ?mOrigen ?mDestino ); debe existir una conexion entre el muelle origen y el muelle destino
        (libre ?g) ; la grua debe estar libre
     )
    :effect (and 
        (not(libre ?g)) ;la grua ya no estar libre
        (en ?c ?g) ; el contenedor esta en la la grua
        (not (en ?c ?t)) ; el contenedor no esta en la cinta
        libre ?t) ; la cinta esta ocupada 
        (en ?c ?mDestino) ;el contenedor ya tiene ubicacion
    )
)


)