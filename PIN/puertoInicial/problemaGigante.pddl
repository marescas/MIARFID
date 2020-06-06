(define (problem problema1) (:domain puerto)
(:objects 
    ;gruas
    g1 - grua
    g2 - grua
    g3 - grua
    g4 - grua
    g5 - grua
    
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
    p13 - pila
    p14 - pila
    p15 - pila

    ;muelles
    m1 - muelle
    m2 - muelle
    m3 - muelle
    m4 - muelle
    m5 - muelle

    ;cintas 
    t12 - cinta
    t21 - cinta
    t13 - cinta
    t31 - cinta
    t14 - cinta
    t41 - cinta
    t15 - cinta
    t51 - cinta

    t23 - cinta
    t32 - cinta
    t24 - cinta
    t42 - cinta
    t25 - cinta
    t52 - cinta

    t34 - cinta
    t43 - cinta
    t35 - cinta
    t53 - cinta

    t45 - cinta
    t54 - cinta

    ;contenedores
    c1 - contenedor
    c2 - contenedor
    c3 - contenedor;contenedorObjetivo
    c4 - contenedor
    c5 - contenedor
    c6 - contenedor
    c7 - contenedor;contenedorObjetivo
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
    c21 - contenedor;contenedorObjetivo
    c22 - contenedor
    c23 - contenedor;contenedorObjetivo
    c24 - contenedor
    c25 - contenedor
    c26 - contenedor
    c27 - contenedor
    c28 - contenedor
    c29 - contenedor
    c30 - contenedor


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
    (en c2 p1)
    (en c26 p1)
    (en c30 p1)
    (en c3 p2)
    (en c4 p2)
    (en c5 p3)
    (en c8 p3)

    ;contenedores pilas muelle 2
    (en c6 p4)
    (en c7 p5)
    (en c9 p5)
    (en c10 p6)
    (en c11 p6)
    (en c24 p6)
    (en c29 p6)

    ;contenedores pilas muelle 3
    (en c12 p7)
    (en c21 p7)
    (en c13 p8)
    (en c25 p8)
    (en c14 p9)

    ;contenedores pilas muelle 4
    (en c15 p10)
    (en c16 p11)
    (en c17 p12)
    (en c22 p12)
    (en c27 p12)

    ;contenedores pilas muelle 5
    (en c18 p13)
    (en c19 p14)
    (en c23 p14)
    (en c20 p15)
    (en c28 p15)

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

    ;pilas en muelle 5
    (en p13 m5)
    (en p14 m5)
    (en p15 m5)

    ;encima para contenedores
    (encima c2 c1)
    (encima c4 c3)
    (encima c8 c5)

    (encima c9 c7)
    (encima c29 c24)
    (encima c24 c11)
    (encima c11 c10)

    (encima c21 c12)
    (encima c25 c13)

    (encima c27 c22)
    (encima c22 c17)

    (encima c23 c19)
    (encima c28 c20)

    ;encima contenedores en pila
    (encima c1 p1)
    (encima c3 p2)
    (encima c5 p3)
    (encima c6 p4)
    (encima c7 p5)
    (encima c10 p6)
    (encima c12 p7)
    (encima c13 p8)
    (encima c14 p9)
    (encima c15 p10)
    (encima c16 p11)
    (encima c17 p12)
    (encima c18 p13)
    (encima c19 p14)
    (encima c20 p15)

    ;gruas en muelles
    (en g1 m1)
    (en g2 m2)
    (en g3 m3)
    (en g4 m4)
    (en g5 m5)

    ;conexiones entre muelles 
    (conecta t12 m1 m2)
    (conecta t21 m2 m1)
    (conecta t13 m1 m3)
    (conecta t31 m3 m1)
    (conecta t14 m1 m4)
    (conecta t41 m4 m1)
    (conecta t15 m1 m5)
    (conecta t51 m5 m1)
    (conecta t23 m2 m3)
    (conecta t32 m3 m2)
    (conecta t24 m2 m4)
    (conecta t42 m4 m2)
    (conecta t25 m2 m5)
    (conecta t52 m5 m2)
    (conecta t34 m3 m4)
    (conecta t43 m4 m3)
    (conecta t35 m3 m5)
    (conecta t53 m5 m3)
    (conecta t45 m4 m5)
    (conecta t54 m5 m4)

    ;cimas
    (top c30 p1)
    (top c4 p2)
    (top c8 p3)
    (top c6 p4)
    (top c9 p5)
    (top c29 p6)
    (top c21 p7)
    (top c25 p8)
    (top c14 p9)
    (top c15 p10)
    (top c16 p11)
    (top c27 p12)
    (top c18 p13)
    (top c23 p14)
    (top c28 p15)

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
    (libre g5)

    (libre t12)
    (libre t21)
    (libre t13)
    (libre t31)
    (libre t14)
    (libre t41)
    (libre t15)
    (libre t51)
    (libre t23)
    (libre t32)
    (libre t24)
    (libre t42)
    (libre t25)
    (libre t52)
    (libre t34)
    (libre t43)
    (libre t35)
    (libre t53)
    (libre t45)
    (libre t54)

    ;altura
    (altura p1 n4)
    (altura p2 n2)
    (altura p3 n2)
    (altura p4 n1)
    (altura p5 n2)
    (altura p6 n4)
    (altura p7 n2)
    (altura p8 n2)
    (altura p9 n1)
    (altura p10 n1)
    (altura p11 n1)
    (altura p12 n3)
    (altura p13 n1)
    (altura p14 n2)
    (altura p15 n2)

    ;disponibilidades
    (disponible c30)
    (disponible c4)
    (disponible c8)
    (disponible c6)
    (disponible c9)
    (disponible c29)
    (disponible c21)
    (disponible c25)
    (disponible c14)
    (disponible c15)
    (disponible c16)
    (disponible c27)
    (disponible c18)
    (disponible c23)
    (disponible c28)

    ;contenedores verdes
    (verde c3)
    (verde c7)
    (verde c10)
    (verde c11)
    (verde c16)
    (verde c17)
    (verde c20)
    (verde c21)
    (verde c23)

    ;contenedores no verde 
    (noverde c1)
    (noverde c2)
    (noverde c4)
    (noverde c5)
    (noverde c6)
    (noverde c8)
    (noverde c9)
    (noverde c12)
    (noverde c13)
    (noverde c14)
    (noverde c15)
    (noverde c18)
    (noverde c19)
    (noverde c22)
    (noverde c24)
    (noverde c25)
    (noverde c26)
    (noverde c27)
    (noverde c28)
    (noverde c29)
    (noverde c30)

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
    (noverde p13)
    (noverde p14)
    (noverde p15)

    ; contenedores en muelle
    (en c1 m1)
    (en c2 m1)
    (en c26 m1)
    (en c30 m1)
    (en c3 m1)
    (en c4 m1)
    (en c5 m1)
    (en c8 m1)

    (en c6 m2)
    (en c7 m2)
    (en c9 m2)
    (en c10 m2)
    (en c11 m2)
    (en c24 m2)
    (en c29 m2)

    (en c12 m3)
    (en c21 m3)
    (en c13 m3)
    (en c25 m3)
    (en c14 m3)

    (en c15 m4)
    (en c16 m4)
    (en c17 m4)
    (en c22 m4)
    (en c27 m4)

    (en c18 m5)
    (en c19 m5)
    (en c23 m5)
    (en c20 m5)
    (en c28 m5)

)

(:goal (and
    (en c3 m1)
    (en c7 m1)
    (en c10 m1)
    (en c11 m1)
    (en c16 m1)
    (en c17 m1)
    (en c20 m1)
    (en c21 m1)
    (en c23 m1)

    (disponible c3)
    (disponible c7)
    (disponible c10)
    (disponible c11)
    (disponible c16)
    (disponible c17)
    (disponible c20)
    (disponible c21)
    (disponible c23)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
