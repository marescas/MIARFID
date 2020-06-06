/**
* Grafo.js
* Carga un grafo de escena en Threejs y lo visualiza
*
*/

var renderer, scene, camera;
var camaraPlanta;
var angulo = 0;
var robot, brazo, antebrazo, mano, base, pinzaI, pinzaD;
var cameraControl;
var keyboard
var updateFcts = [];
const L = 110
init();
loadScene();
setupGUI();
render();

function init() {
    // inicializar Threejs

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0x0000AA));
    renderer.autoClear = false
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();
    setCameras(window.innerWidth / window.innerHeight)

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(90, 200, 350);
    camera.lookAt(new THREE.Vector3(0, 0, 0));
    cameraControls = new THREE.OrbitControls(camera, renderer.domElement);
    cameraControls.noKeys = true;
    cameraControls.target.set(0, 0, 0);
    window.addEventListener("resize", updateAspectRatio)

}

function loadScene() {
    // Carga la escena
    robot = new THREE.Object3D();
    var geoBase = new THREE.CylinderGeometry(50, 50, 15, 32);
    var matRobot = new THREE.MeshBasicMaterial({ color: 'yellow', wireframe: true });
    var geoEje = new THREE.CylinderGeometry(20, 20, 18, 32);
    var geoEsparrago = new THREE.BoxGeometry(18, 120, 12);
    var geoRotula = new THREE.SphereGeometry(20, 30, 15);
    var geoDisco = new THREE.CylinderGeometry(22, 22, 6, 32);
    var geoNervio = new THREE.BoxGeometry(4, 80, 4);
    var geoMano = new THREE.CylinderGeometry(15, 15, 40, 32);
    var suelo = new THREE.PlaneGeometry(1000, 1000, 50, 50)


    base = new THREE.Mesh(geoBase, matRobot);
    base.position.set(0, 0, 0);

    //Creamos un brazo
    brazo = new THREE.Object3D();
    //Añadimos el eje
    var eje = new THREE.Mesh(geoEje, matRobot)
    eje.rotateZ(Math.PI / 2);
    brazo.add(eje);
    //Añadimos el esparrago
    var esparrago = new THREE.Mesh(geoEsparrago, matRobot)
    esparrago.rotateY(Math.PI / 2);
    esparrago.position.set(0, 50, 0)
    brazo.add(esparrago)
    //Añadimos la rotula
    var rotula = new THREE.Mesh(geoRotula, matRobot)
    rotula.position.set(0, 120, 0)
    brazo.add(rotula);

    //Creamos un antebrazo
    antebrazo = new THREE.Object3D();
    //Disco
    disco = new THREE.Mesh(geoDisco, matRobot);

    //Nervio1
    nervio1 = new THREE.Mesh(geoNervio, matRobot);
    nervio1.position.set(8, 34, -4)

    //Nervio2
    nervio2 = new THREE.Mesh(geoNervio, matRobot);
    nervio2.position.set(-8, 34, -4)


    //Nervio3
    nervio3 = new THREE.Mesh(geoNervio, matRobot);
    nervio3.position.set(8, 34, 4)

    //Nervio4
    nervio4 = new THREE.Mesh(geoNervio, matRobot);
    nervio4.position.set(-8, 34, 4)
    antebrazo.add(nervio4);

    //mano 
    mano = new THREE.Mesh(geoMano, matRobot)
    mano.position.set(0, 70, 5);
    mano.rotateZ(Math.PI / 2)

    antebrazo.position.set(0, 120, 0)

    //Geometria de la pinza
    geopinza = new THREE.Geometry();
    geopinza.vertices.push(
        new THREE.Vector3(0, -8, -10), //0
        new THREE.Vector3(19, -8, -10), //1
        new THREE.Vector3(0, -8, 10), //2
        new THREE.Vector3(19, -8, 10), //3
        new THREE.Vector3(0, -12, -10), //4
        new THREE.Vector3(19, -12, -10), //5
        new THREE.Vector3(0, -12, 10), //6
        new THREE.Vector3(19, -12, 10), //7
        new THREE.Vector3(38, -8, -5), //8
        new THREE.Vector3(38, -12, -5), //9
        new THREE.Vector3(38, -8, 5), //10
        new THREE.Vector3(38, -12, 5), //11
    );
    geopinza.faces.push(
        new THREE.Face3(0, 3, 2),
        new THREE.Face3(0, 1, 3),
        new THREE.Face3(1, 7, 3),
        new THREE.Face3(1, 5, 7),
        new THREE.Face3(5, 6, 7),
        new THREE.Face3(5, 4, 6),
        new THREE.Face3(4, 2, 6),
        new THREE.Face3(4, 0, 2),
        new THREE.Face3(2, 7, 6),
        new THREE.Face3(2, 3, 7),
        new THREE.Face3(4, 1, 0),
        new THREE.Face3(4, 5, 1),
        new THREE.Face3(1, 10, 3),
        new THREE.Face3(1, 8, 10),
        new THREE.Face3(8, 11, 10),
        new THREE.Face3(8, 9, 11),
        new THREE.Face3(9, 7, 11),
        new THREE.Face3(9, 5, 7),
        new THREE.Face3(3, 11, 7),
        new THREE.Face3(3, 10, 11),
        new THREE.Face3(5, 8, 1),
        new THREE.Face3(5, 9, 8),
    )
    pinzaI = new THREE.Mesh(geopinza, matRobot);
    pinzaI.rotateY(Math.PI / 2)
    pinzaD = new THREE.Mesh(geopinza, matRobot);
    pinzaD.rotateY(Math.PI / 2)
    pinzaD.position.set(0, 20, 0)

    //Grafo de escena

    antebrazo.add(disco);
    antebrazo.add(nervio1);
    antebrazo.add(nervio2);
    antebrazo.add(nervio3);
    brazo.add(antebrazo)
    antebrazo.add(mano)
    mano.add(pinzaI)
    mano.add(pinzaD)

    robot.add(base)
    base.add(brazo)
    scene.add(robot)

    scene.add(new THREE.AxesHelper(1000));

    //Suelo
    //Coordinates.drawGround({ size: 10000, offset: -10, wireframe: true });
    var miSuelo = new THREE.Mesh(suelo, matRobot)
    miSuelo.rotateX(-Math.PI / 2)
    scene.add(miSuelo)
    keyboard = new THREEx.KeyboardState(renderer.domElement);
    renderer.domElement.setAttribute("tabIndex", "0");
    renderer.domElement.focus();
    keyboard.domElement.addEventListener('keydown', function (event) {
        if (keyboard.eventMatches(event, 'left')) {
            robot.position.x -= 10;
        }
        if (keyboard.eventMatches(event, 'right')) {
            robot.position.x += 10;
        }
        if (keyboard.eventMatches(event, 'up')) {
            robot.position.z -= 10;
        }
        if (keyboard.eventMatches(event, 'down')) {
            robot.position.z += 10;
        }
    })


}

function updateAspectRatio() {
    //ajustar la camara y el viewport a las nuevas dimensiones del canvas
    renderer.setSize(window.innerWidth, window.innerHeight);
    var aspectRatio = window.innerWidth / window.innerHeight;
    camera.aspect = aspectRatio

    if (aspectRatio < 1) {
        camaraPlanta.left = -L
        camaraPlanta.right = L
        camaraPlanta.top = L;
        camaraPlanta.bottom = -L
    } else {
        camaraPlanta.left = -L
        camaraPlanta.right = L
        camaraPlanta.top = L;
        camaraPlanta.bottom = -L
    }
    camaraPlanta.updateProjectionMatrix()
    camera.updateProjectionMatrix()
}
function render() {
    requestAnimationFrame(render);
    renderer.domElement.setAttribute("tabIndex", "0");
    renderer.domElement.focus();
    update()
    renderer.domElement.focus();
    renderer.clear()
    renderer.setViewport(0, 0, window.innerWidth, window.innerHeight)
    renderer.render(scene, camera);
    renderer.setViewport(0, 0, Math.min(window.innerWidth, window.innerHeight) / 4, Math.min(window.innerWidth, window.innerHeight) / 4)

    renderer.render(scene, camaraPlanta)
}
function update() {
    base.rotation.y = effectControl.giroBase * Math.PI / 2
    brazo.rotation.z = effectControl.giroBrazo * Math.PI / 180
    antebrazo.rotation.z = effectControl.giroAntebrazoY * Math.PI / 180
    antebrazo.rotation.y = effectControl.giroAntebrazoZ * Math.PI / 180
    mano.rotation.x = effectControl.giroPinzaZ * Math.PI / 180
    pinzaI.position.y = 25 - effectControl.aperturaPinza / 2 - 3
    pinzaD.position.y = effectControl.aperturaPinza / 2 + 3

}
function setCameras(ar) {
    //configurar planta alsado, perfil y perspectiva 
    var camaraOrtografica
    camaraOrtografica = new THREE.OrthographicCamera(-L, L, L, -L, -1, 800);
    camaraOrtografica.lookAt(new THREE.Vector3(0, 0, 0));

    camaraPlanta = camaraOrtografica.clone()
    camaraPlanta.position.set(0, L, 0);
    camaraPlanta.up = new THREE.Vector3(0, 0, -1)
    camaraPlanta.lookAt(new THREE.Vector3(0, 0, 0))
    var camaraPerspectiva = new THREE.PerspectiveCamera(75, ar, 0.1, 100);
    camaraPerspectiva.position.set(1, 2, 10);
    camaraPerspectiva.lookAt(new THREE.Vector3(0, 0, 0))
    camera = camaraPerspectiva.clone()
    scene.add(camera)
    scene.add(camaraPlanta)

}
function setupGUI() {

    //Interfaz de usuario
    effectControl = {
        giroBase: 0,
        giroBrazo: 0,
        giroAntebrazoZ: 0,
        giroAntebrazoY: 0,
        giroPinzaZ: 0,
        aperturaPinza: 0,
        reiniciar: function () {
            angulo = 0
            location.reload();
        },
        color: "rgb(255,255,0)"
    }
    var gui = new dat.GUI();
    var sub = gui.addFolder("Controles Robot")
    sub.add(effectControl, "giroBase", -180, 180, 1).name("Giro Base");
    sub.add(effectControl, "giroBrazo", -45, 45, 1).name("Giro Brazo");
    sub.add(effectControl, "giroAntebrazoZ", -180, 180, 1).name("Giro Antebrazo Z");
    sub.add(effectControl, "giroAntebrazoY", -90, 90, 1).name("Giro Antebrazo Y");
    sub.add(effectControl, "giroPinzaZ", -40, 220, 1).name("Giro Pinza");
    sub.add(effectControl, "aperturaPinza", 0, 15, 1).name("Cierre pinza");

    sub.add(effectControl, "reiniciar")
    var sensorColor = sub.addColor(effectControl, "color").name("Color")
    sensorColor.onChange(function (color) {
        robot.traverse(function (hijo) {
            if (hijo instanceof THREE.Mesh) {
                hijo.material.color = new THREE.Color(color)
            }
        })
    })


}
