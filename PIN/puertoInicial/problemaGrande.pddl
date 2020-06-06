(define (problem problema1) (:domain puerto)
(:objects 
    ;gruas
    g1 - grua
    g2 - grua
    g3 - grua
    g4 - grua
    
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
    p10 - pila
    p11 - pila
    p12 - pila

    ;muelles
    m1 - muelle
    m2 - muelle
    m3 - muelle
    m4 - muelle

    ;cintas 
    t12 - cinta
    t21 - cinta
    t13 - cinta
    t31 - cinta
    t14 - cinta
    t41 - cinta

    t23 - cinta
    t32 - cinta
    t24 - cinta
    t42 - cinta

    t34 - cinta
    t43 - cinta

    ;contenedores
    c1 - contenedor
    c2 - contenedor
    c3 - contenedor;contenedorObjetivo
    c4 - contenedor;contenedorObjetivo
    c5 - contenedor
    c6 - contenedor
    c7 - contenedor
    c8 - contenedor
    c9 - contenedor
    c10 - contenedor;contenedorObjetivo
    c11 - contenedor;contenedorObjetivo
    c12 - contenedor
    c13 - contenedor
    c14 - contenedor
    c15 - contenedor
    c16 - contenedor;contenedorObjetivo
    c17 - contenedor;contenedorObjetivo
    c18 - contenedor
    c19 - contenedor
    c20 - contenedor;contenedorObjetivo

    ;niveles 
    n0 - nivel
    n1 - nivel
    n2 - nivel
    n3 - nivel
    n4 - nivel
) 

(:init
    ;contenedores pilas muelle 1
    (en c1 p1)
    (en c3 p2)
    (en c5 p2)
    (en c18 p3)

    ;contenedores pilas muelle 2
    (en c14 p4)
    (en c11 p5)
    (en c10 p5)
    (en c15 p5)
    (en c8 p5)
    (en c7 p6)

    ;contenedores pilas muelle 3
    (en c13 p7)
    (en c2 p8)
    (en c4 p8)
    (en c17 p9)
    (en c6 p9)

    ;contenedores pilas muelle 4
    (en c12 p10)
    (en c9 p10)
    (en c20 p11)
    (en c19 p12)
    (en c16 p12)

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

    ;pilas en muelle 4
    (en p10 m4)
    (en p11 m4)
    (en p12 m4)

    ;encima para contenedores
    (encima c5 c3)
    (encima c8 c15)
    (encima c15 c10)
    (encima c10 c11)
    (encima c4 c2)
    (encima c6 c17)
    (encima c9 c12)
    (encima c16 c19)

    ;encima contenedores en pila
    (encima c1 p1)
    (encima c3 p2)
    (encima c18 p3)
    (encima c14 p4)
    (encima c11 p5)
    (encima c7 p6)
    (encima c13 p7)
    (encima c2 p8)
    (encima c17 p9)
    (encima c12 p10)
    (encima c20 p11)
    (encima c19 p12)

    ;gruas en muelles
    (en g1 m1)
    (en g2 m2)
    (en g3 m3)
    (en g4 m4)

    ;conexiones entre muelles 
    (conecta t12 m1 m2)
    (conecta t21 m2 m1)
    (conecta t13 m1 m3)
    (conecta t31 m3 m1)
    (conecta t14 m1 m4)
    (conecta t41 m4 m1)
    (conecta t23 m2 m3)
    (conecta t32 m3 m2)
    (conecta t24 m2 m4)
    (conecta t42 m4 m2)
    (conecta t34 m3 m4)
    (conecta t43 m4 m3)

    ;cimas
    (top c1 p1)
    (top c5 p2)
    (top c18 p3)
    (top c14 p4)
    (top c8 p5)
    (top c7 p6)
    (top c13 p7)
    (top c4 p8)
    (top c6 p9)
    (top c9 p10)
    (top c20 p11)
    (top c16 p12)

    ;next con altura maxima 4
    (next n0 n1)
    (next n1 n2)
    (next n2 n3)
    (next n3 n4)

    ;libre cinta y grua
    (libre g1)
    (libre g2)
    (libre g3)
    (libre g4)

    (libre t12)
    (libre t21)
    (libre t13)
    (libre t31)
    (libre t14)
    (libre t41)
    (libre t23)
    (libre t32)
    (libre t24)
    (libre t42)
    (libre t34)
    (libre t43)

    ;altura
    (altura p1 n1)
    (altura p2 n2)
    (altura p3 n1)
    (altura p4 n1)
    (altura p5 n4)
    (altura p6 n1)
    (altura p7 n1)
    (altura p8 n2)
    (altura p9 n2)
    (altura p10 n2)
    (altura p11 n1)
    (altura p12 n2)

    ;disponibilidades
    (disponible c1)
    (disponible c5)
    (disponible c18)
    (disponible c14)
    (disponible c8)
    (disponible c7)
    (disponible c13)
    (disponible c4)
    (disponible c6)
    (disponible c9)
    (disponible c20)
    (disponible c16)

    ;contenedores verdes
    (verde c3)
    (verde c4)
    (verde c10)
    (verde c11)
    (verde c16)
    (verde c17)
    (verde c20)

    ;contenedores no verde 
    (noverde c1)
    (noverde c2)
    (noverde c5)
    (noverde c6)
    (noverde c7)
    (noverde c8)
    (noverde c9)
    (noverde c12)
    (noverde c13)
    (noverde c14)
    (noverde c15)
    (noverde c18)
    (noverde c19)

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
    (noverde p10)
    (noverde p11)
    (noverde p12)

    ; contenedores en muelle
    (en c1 m1)
    (en c3 m1)
    (en c5 m1)
    (en c18 m1)

    (en c14 m2)
    (en c11 m2)
    (en c10 m2)
    (en c15 m2)
    (en c8 m2)
    (en c7 m2)

    (en c13 m3)
    (en c2 m3)
    (en c4 m3)
    (en c17 m3)
    (en c6 m3)

    (en c12 m4)
    (en c9 m4)
    (en c20 m4)
    (en c19 m4)
    (en c16 m4)

)

(:goal (and
    (en c3 m1)
    (en c4 m1)
    (en c10 m1)
    (en c11 m1)
    (en c16 m1)
    (en c17 m1)
    (en c20 m1)   

    (disponible c3)
    (disponible c4)
    (disponible c10)
    (disponible c11)
    (disponible c16)
    (disponible c17)
    (disponible c20)

))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
