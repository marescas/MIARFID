(define (problem problema1) (:domain puerto)
(:objects 
    ;gruas
    g1 - grua
    g2 - grua
    g3 - grua
    
    ;pilas
    p1 - pila
    p2 - pila
    p3 - pila
    p4 - pila
    p5 - pila
    p6 - pila
    p7 - pila
    p8 - pila
    p9 - pila

    ;muelles
    m1 - muelle
    m2 - muelle
    m3 - muelle

    ;cintas 
    t12 - cinta
    t21 - cinta
    t13 - cinta
    t31 - cinta
    t23 - cinta
    t32 - cinta

    ;contenedores
    c1 - contenedor
    c2 - contenedor
    c3 - contenedor;contenedorObjetivo
    c4 - contenedor;contenedorObjetivo
    c5 - contenedor
    c6 - contenedor;contenedorObjetivo
    c7 - contenedor
    c8 - contenedor;contenedorObjetivo
    c9 - contenedor
    c10 - contenedor
    c11 - contenedor
    c12 - contenedor;contenedorObjetivo
    c13 - contenedor
    c14 - contenedor
    c15 - contenedor
    c16 - contenedor

    ;niveles 
    n0 - nivel
    n1 - nivel
    n2 - nivel
    n3 - nivel
) 

(:init
    ;contenedores pilas muelle 1
    (en c1 p1)
    (en c4 p1)
    (en c3 p2)
    (en c7 p2)
    (en c10 p2)
    (en c2 p3)

    ;contenedores pilas muelle 2
    (en c15 p4)
    (en c5 p5)
    (en c11 p5)
    (en c6 p6)

    ;contenedores pilas muelle 3
    (en c16 p7)
    (en c13 p7)
    (en c8 p8)
    (en c9 p8)
    (en c12 p9)
    (en c14 p9)

    ;pilas en muelle 1
    (en p1 m1)
    (en p2 m1)
    (en p3 m1)

    ;pilas en muelle 2
    (en p4 m2)
    (en p5 m2)
    (en p6 m2)

    ;pilas en muelle 3
    (en p7 m3)
    (en p8 m3)
    (en p9 m3)

    ;encima para contenedores
    (encima c4 c1)
    (encima c10 c7)
    (encima c7 c3)
    (encima c11 c5)
    (encima c13 c16)
    (encima c9 c8)
    (encima c14 c12)

    ;encima contenedores en pila
    (encima c1 p1)
    (encima c3 p2)
    (encima c2 p3)
    (encima c15 p4)
    (encima c5 p5)
    (encima c6 p6)
    (encima c16 p7)
    (encima c8 p8)
    (encima c12 p9)

    ;gruas en muelles
    (en g1 m1)
    (en g2 m2)
    (en g3 m3)

    ;conexiones entre muelles 
    (conecta t12 m1 m2)
    (conecta t21 m2 m1)
    (conecta t13 m1 m3)
    (conecta t31 m3 m1)
    (conecta t23 m2 m3)
    (conecta t32 m3 m2)

    ;cimas
    (top c4 p1)
    (top c10 p2)
    (top c2 p3)
    (top c15 p4)
    (top c11 p5)
    (top c6 p6)
    (top c13 p7)
    (top c9 p8)
    (top c14 p9)

    ;next con altura maxima 3
    (next n0 n1)
    (next n1 n2)
    (next n2 n3)

    ;libre cinta y grua
    (libre g1)
    (libre g2)
    (libre g3)
    (libre t12)
    (libre t21)
    (libre t13)
    (libre t31)
    (libre t23)
    (libre t32)

    ;altura
    (altura p1 n2)
    (altura p2 n3)
    (altura p3 n1)
    (altura p4 n1)
    (altura p5 n2)
    (altura p6 n1)
    (altura p7 n2)
    (altura p8 n2)
    (altura p9 n2)

    ;disponibilidades
    (disponible c4)
    (disponible c10)
    (disponible c2)
    (disponible c15)
    (disponible c11)
    (disponible c6)
    (disponible c13)
    (disponible c9)
    (disponible c14)

    ;contenedores verdes
    (verde c3)
    (verde c4)
    (verde c6)
    (verde c8)
    (verde c12)

    ;contenedores no verde 
    (noverde c1)
    (noverde c2)
    (noverde c5)
    (noverde c7)
    (noverde c9)
    (noverde c10)
    (noverde c11)
    (noverde c13)
    (noverde c14)
    (noverde c15)
    (noverde c16)

    ;pilas no verdes
    (noverde p1)
    (noverde p2)
    (noverde p3)
    (noverde p4)
    (noverde p5)
    (noverde p6)
    (noverde p7)
    (noverde p8)
    (noverde p9)

    ; contenedores en muelle
    (en c1 m1)
    (en c4 m1)
    (en c3 m1)
    (en c7 m1)
    (en c10 m1)
    (en c2 m1)

    (en c15 m2)
    (en c5 m2)
    (en c11 m2)
    (en c6 m2)

    (en c16 m3)
    (en c13 m3)
    (en c8 m3)
    (en c9 m3)
    (en c12 m3)
    (en c14 m3)
)

(:goal (and
    (en c3 m1)
    (en c4 m1)
    (en c6 m1)
    (en c8 m1)
    (en c12 m1)

    (disponible c3)
    (disponible c4)
    (disponible c6)
    (disponible c8)
    (disponible c12)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
