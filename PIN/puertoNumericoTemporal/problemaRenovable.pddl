(define (problem problema1) (:domain puerto)
(:objects 
    ;gruas
    g1 - grua
    g2 - grua
    ;pilas
    p1 - pila
    p2 - pila
    p3 - pila
    p4 - pila
    p5 - pila
    p6 - pila
    ;muelles
    m1 - muelle
    m2 - muelle
    ;cintas 
    t1 - cinta
    t2 - cinta
    ;contenedores
    c1 - contenedor
    c2 - contenedor
    c3 - contenedor;contenedorObjetivo
    c4 - contenedor;contenedorObjetivo
    c5 - contenedor
    c6 - contenedor
    c7 - contenedor;contenedorObjetivo
    c8 - contenedor
    c9 - contenedor
    c10 - contenedor
    c11 - contenedor
    ;niveles 
    n0 - nivel
    n1 - nivel
    n2 - nivel
    n3 - nivel
)
;etiqueta verde (predicado)TODO 

(:init
    ;contenedores pilas muelle 1
    (en c1 p1)
    (en c7 p1)
    (en c9 p2)
    (en c10 p2)
    (en c11 p3)
    ;contenedores pilas muelle 2
    (en c4 p4)
    (en c8 p4)
    (en c5 p5)
    (en c3 p5)
    (en c2 p5)
    (en c6 p6)
    ;pilas en muelle 1
    (en p1 m1)
    (en p2 m1)
    (en p3 m1)
    ;pilas en muelle 2
    (en p4 m2)
    (en p5 m2)
    (en p6 m2)
    ;encima para contenedores
    (encima c7 c1)
    (encima c10 c9)
    (encima c8 c4 )
    (encima c2 c3)
    (encima c3 c5)
    ;encima contenedores en pila
    (encima c1 p1)
    (encima c9 p2 )
    (encima c11 p3)
    (encima c4 p4)
    (encima c5 p5)
    (encima  c6 p6)
    ;grua en muelle 1
    (en g1 m1)
    ;grua  en muelle 2
    (en g2 m2)
    ;conexiones entre muelles 
    (conecta t1 m1 m2)
    (conecta t2 m2 m1)
    ;cimas
    (top c7 p1)
    (top c10 p2)
    (top c11 p3)
    (top c8 p4)
    (top c2 p5 )
    (top c6 p6)
    ;next con altura maxima 3
    (next n0 n1)
    (next n1 n2)
    (next n2 n3)
    ;libre cinta y grua
    (libre g1)
    (libre g2)
    (libre t1)
    (libre t2)
    ;altura
    (altura p1 n2)
    (altura p2 n2)
    (altura p3 n1)
    (altura p4 n2)
    (altura p5 n3)
    (altura p6 n1)
    ;disponibilidades
    (disponible c7)
    (disponible c10)
    (disponible c11)
    (disponible c8)
    (disponible c2)
    (disponible c6)
    ;contenedores verdes
    (verde c3)
    (verde c4)
    (verde c7)
    ;contenedores no verde 
    (noverde c1)
    (noverde c2)
    (noverde c6)
    (noverde c5)
    (noverde c8)
    (noverde c9)
    (noverde c10)
    (noverde c11)
    ;pilas no verdes
    (noverde p1)
    (noverde p2)
    (noverde p3)
    (noverde p4)
    (noverde p5)
    (noverde p6)
    ; contenedores en muelle
    (en c7 m1)
    (en c1 m1)
    (en c10 m1)
    (en c9 m1)
    (en c11 m1)
    (en c4 m2)
    (en c2 m2)
    (en c8 m2)
    (en c3 m2)
    (en c5 m2)
    (en c6 m2)
    ;pesos de contenedor
    (= (peso c1) 5)
    (= (peso c2) 2)
    (= (peso c3) 3)
    (= (peso c4) 6)
    (= (peso c5) 5)
    (= (peso c6) 5)
    (= (peso c7) 5)
    (= (peso c8) 5)
    (= (peso c9) 10)
    (= (peso c10) 8)
    (= (peso c11) 5)
    ;alturas pilas
    (= (conaltura n0) 1)
    (= (conaltura n1) 2)
    (= (conaltura n2) 3)
    (= (conaltura n3) 4)
    ;tiempo de transportar un contenedor en la cinta
    (= (tiempoTransporteLento) 10)
    (= (tiempoTransporteRapido) 5)
    (= (consumoTransporteLento) 50)
    (= (consumoTransporteRapido) 100)
    ;
    (= (gasolinaDisponible) 400)
    (= (totalGastado) 0)
    (= (tamanyoDeposito) 400)
    (= (tiempoRepostar) 20)
        

    




)

(:goal (and
    (en c3 m1)
    (en c4 m1)
    (en c7 m1)
    (disponible c3)
    (disponible c4)
    (disponible c7)
))

;metrica a minimizar
(:metric minimize (total-time))
)
