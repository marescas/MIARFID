/**
*
* Proyecto final GPC
* Marcos Esteve Casademunt
*/

var render, scene, camera, camaraPlanta;
var epsilon = 0.0
var angulo = 0;
var cameraControls;
var keyboard
var world, reloj
var numeroMaximoMonedas = 2
var numeroMonedas = 0
var monedas_recogidas = 0
var scale = 1;
var mouseX = 0;
var mouseY = 0;
var monedas = []
var antes = Date.now()
var linterna
var finJuego = false
const L = 11
data = [[true, true, true, true, true, true, true, true, true, true, true], [true, false, false, false, false, false, false, false, false, false, true], [true, false, true, true, true, true, true, true, true, false, true], [true, false, true, false, false, false, false, false, false, false, true], [true, false, true, true, true, false, true, true, true, false, true], [true, false, false, false, true, false, true, false, false, false, true], [true, true, true, true, true, false, true, false, true, false, true], [true, false, false, false, false, false, false, false, true, false, true], [true, true, true, true, true, true, true, true, true, false, true], [true, false, false, false, false, false, false, false, false, false, true], [true, true, true, true, true, true, true, true, true, true, true]]
var monedas
var monedasObjetcs = []
var target
var light
var material, materialSuelo
var cameraControlsActivado = false
var effectControl
var focal
var adelante = 0
init();
setupGUI()
loadScene();
render();



function setupGUI() {

    //Interfaz de usuario
    effectControl = {
        niebla: 0.0,
        luz: 0.0,
        posicionLuz: 0.0
    }
    var gui = new dat.GUI();
    var sub = gui.addFolder("Controles laberinto")
    sub.add(effectControl, "niebla", 0.0, 3, 0.05).name("Niebla");
    sub.add(effectControl, "luz", 0.0, 2.0, 0.1).name("Luz");
    sub.add(effectControl, "posicionLuz", 0.0, 180, 1).name("Posicion Luz");



}
function init() {

    //console.log(monedas)
    //Inicializar en Threejs

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0x0000AA));
    renderer.autoClear = false
    renderer.shadowMap.enabled = true;
    document.getElementById('container').appendChild(renderer.domElement);
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();
    {
        const color = 0xFFFFFF;
        const density = 0.2;
        scene.fog = new THREE.FogExp2(color, density);
    }
    setCameras(window.innerWidth / window.innerHeight)
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 100000);
    camera.position.set(5, 0.5, 5);
    camera.lookAt(new THREE.Vector3(0, 0, 0));
    camera.rotation.order = "YXZ";

    window.addEventListener("resize", updateAspectRatio)
    var ambiental = new THREE.AmbientLight(0x444444);
    scene.add(ambiental);
    focal = new THREE.SpotLight('white', 1);
    focal.position.set(50, 50, 50);
    focal.target.position.set(0, 0, 0);
    focal.angle = Math.PI / 2;
    focal.penumbra = 0.2;

    focal.shadow.camera.near = 2;
    focal.shadow.camera.far = 1000;
    //focal.shadow.camera.fov = 100;
    //focal.shadow.mapSize.width = 500;
    //focal.shadow.mapSize.height = 500;

    focal.castShadow = true;
    scene.add(focal);
    //scene.add(new THREE.CameraHelper(focal.shadow.camera));



}

function creaPeonza() {
    //var material2 = new THREE.MeshPhongMaterial({ color: 'yellow', specular: 0x99BBFF, shininess: 50 });
    material2 = new THREE.MeshBasicMaterial({ wireframe: true })
    //GEOMETRIA Peonza
    var cuerpo = new THREE.Mesh(new THREE.CylinderGeometry(1, 0.2, 2, 10, 2), material2)
    var punta = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0, 0.5, 10, 2), material2)
    var mango = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.5, 10, 2), material2)
    var peonza = new THREE.Object3D();
    cuerpo.position.y = 1.5;
    punta.position.y = 0.25;
    mango.position.y = 2.75
    cuerpo.receiveShadow = true;
    cuerpo.castShadow = true;
    punta.receiveShadow = true;
    punta.castShadow = true;
    mango.receiveShadow = true;
    mango.castShadow = true;
    peonza.add(cuerpo)
    peonza.add(mango);
    peonza.add(punta)

    return peonza
}

function loadScene() {

    var loader = new THREE.ObjectLoader();
    var textureLoader = new THREE.TextureLoader()
    // material = new THREE.MeshBasicMaterial({ color: "yellow" })
    //var materialSuelo = new THREE.MeshBasicMaterial({ color: "blue" })
    var texturaMuro = new THREE.TextureLoader().load('images/muro.png');
    //material = new THREE.MeshLambertMaterial({ color: "white", map: texturaMuro, side: THREE.DoubleSide })
    material = new THREE.MeshBasicMaterial({ wireframe: true })
    var texturaSuelo = new THREE.TextureLoader().load('images/suelo.jpeg');
    //materialSuelo = new THREE.MeshLambertMaterial({ color: "white", map: texturaSuelo, side: THREE.DoubleSide })
    materialSuelo = new THREE.MeshBasicMaterial({ wireframe: true })

    reloj = new THREE.Clock();
    reloj.start();

    var geocubo = new THREE.BoxGeometry(1, 2, 1)
    var suelo = new THREE.PlaneGeometry(1000, 1000, 100, 100)

    monedas = [];
    for (var i = 0; i < data.length; i++) {
        monedas[i] = [];
        for (var j = 0; j < data[i].length; j++) {
            monedas[i][j] = null;
        }
    }
    //Cargamos el laberinto y las monedas (peonzas)
    for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < data[i].length; j++) {
            if (data[i][j]) {
                monedas[i][j] = null
                //var cubo = new THREE.Mesh(geocubo, material)
                var cubo = new THREE.Mesh(geocubo, material);
                cubo.receiveShadow = true;
                cubo.castShadow = true;
                cubo.position.set(i, 1, j);
                scene.add(cubo)
            } else {
                if (Math.random() > 0.9 && numeroMonedas < numeroMaximoMonedas) {
                    var peonza = creaPeonza()
                    peonza.position.set(i, 0, j);
                    peonza.scale.set(0.15, 0.15, 0.15);
                    monedas[i][j] = peonza
                    numeroMonedas++;
                }
            }
        }
    }

    //dibujamos el suelo
    var miSuelo = new THREE.Mesh(suelo, material)
    miSuelo.receiveShadow = true;
    miSuelo.rotateX(-Math.PI / 2)
    miSuelo.position.y = 0
    scene.add(miSuelo)
    for (let index = 0; index < monedas.length; index++) {
        for (let j = 0; j < monedas[index].length; j++) {
            var objeto = monedas[index][j];
            if (objeto != null) {
                scene.add(objeto);
            }
        }
    }

    keyboard = new THREEx.KeyboardState(renderer.domElement);
    renderer.domElement.setAttribute("tabIndex", "0");
    renderer.domElement.focus();

    //Dibujamos la habitación
    path = "images/"
    var paredes = [path + "posx1.jpg", path + "negx1.jpg", path + "posy1.jpg", path + "negy1.jpg", path + "posz1.jpg", path + "negz1.jpg"];

    var mapaEntorno = new THREE.CubeTextureLoader().load(paredes);
    var shader = THREE.ShaderLib.cube;
    shader.uniforms.tCube.value = mapaEntorno;

    var matParedes = new THREE.ShaderMaterial(
        {
            fragmentShader: shader.fragmentShader,
            vertexShader: shader.vertexShader,
            uniforms: shader.uniforms,
            depthWrite: false,
            side: THREE.BackSide
        }
    );

    var habitacion = new THREE.Mesh(new THREE.BoxGeometry(10000, 10000, 10000), matParedes);
    scene.add(habitacion);


}
function setCameras(ar) {
    //configurar planta alsado, perfil y perspectiva 
    var camaraOrtografica
    camaraOrtografica = new THREE.OrthographicCamera(-L / 10, L, L / 10, -L, -1, 100);
    camaraOrtografica.lookAt(new THREE.Vector3(0, 0, 0));

    camaraPlanta = camaraOrtografica.clone()
    camaraPlanta.position.set(0, L, 0);
    camaraPlanta.up = new THREE.Vector3(0, 0, -1)
    camaraPlanta.lookAt(new THREE.Vector3(0, 0, 0))
    var camaraPerspectiva = new THREE.PerspectiveCamera(75, ar, 0.1, 100);
    camaraPerspectiva.position.set(5, 0.5, 5);
    camaraPerspectiva.lookAt(new THREE.Vector3(0, 0, 0))
    camera = camaraPerspectiva.clone()

    scene.add(camera)
    scene.add(camaraPlanta)

}

function update() {
    scene.fog = new THREE.FogExp2("white", effectControl.niebla / 3);
    focal.intensity = effectControl.luz
    focal.position.set(effectControl.posicionLuz, 50, effectControl.posicionLuz)
    var ahora = Date.now();
    angulo += 1 * 2 * Math.PI * (ahora - antes) / 1000;
    for (let index = 0; index < monedas.length; index++) {
        for (let j = 0; j < monedas[index].length; j++) {
            var objeto = monedas[index][j];

            if (objeto !== null) {
                objeto.rotation.z = 0.1
                objeto.rotation.y = angulo

            }
        }

    }

    antes = ahora;
    if (!cameraControlsActivado && monedas[Math.round(camera.position.x)][Math.round(camera.position.z)] != null) {
        document.getElementById('info').innerHTML = '¡Has recogido una peonza!';
        monedas[Math.round(camera.position.x)][Math.round(camera.position.z)].scale.set(0.001, 0.001, 0.001)
        monedas[Math.round(camera.position.x)][Math.round(camera.position.z)] = null
        monedas_recogidas += 1
        setTimeout(function () { document.getElementById('info').innerHTML = ''; }, 1000);
    }
    if (!cameraControlsActivado && monedas_recogidas == numeroMonedas && !finJuego) {
        document.getElementById('info').innerHTML = '¡¡¡Ganaste!!!';
        finJuego = true
        setTimeout(function () { document.getElementById('info').innerHTML = ''; }, 2000);
    }


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
keyboard.domElement.addEventListener('keydown', function (event) {
    if (keyboard.eventMatches(event, 'a')) {
        var valorx = camera.position.x - Math.cos(camera.rotation.y) * 0.1;
        var valorz = camera.position.z + Math.sin(camera.rotation.y) * 0.1;
        if (!data[Math.round(valorx + epsilon)][Math.round(valorz + epsilon)]) {
            camera.position.x = valorx
            camera.position.z = valorz
        }
    }
    if (keyboard.eventMatches(event, 'd')) {
        var valorx = camera.position.x + Math.cos(camera.rotation.y) * 0.1;
        var valorz = camera.position.z - Math.sin(camera.rotation.y) * 0.1;
        if (!data[Math.round(valorx + epsilon)][Math.round(valorz + epsilon)]) {
            camera.position.x = valorx
            camera.position.z = valorz
        }
    }
    if (keyboard.eventMatches(event, 'w')) {
        var valorx = camera.position.x - Math.sin(camera.rotation.y) * 0.1;
        var valorz = camera.position.z - Math.cos(camera.rotation.y) * 0.1;
        if (!data[Math.round(valorx + epsilon)][Math.round(valorz + epsilon)]) {
            camera.position.x = valorx
            camera.position.z = valorz
        }
    }
    if (keyboard.eventMatches(event, 's')) {
        var valorx = camera.position.x + Math.sin(camera.rotation.y) * 0.1;
        var valorz = camera.position.z + Math.cos(camera.rotation.y) * 0.1;
        if (!data[Math.round(valorx + epsilon)][Math.round(valorz + epsilon)]) {

            camera.position.x = valorx
            camera.position.z = valorz
        }
    }
    if (keyboard.eventMatches(event, 's')) {
        var valorx = camera.position.x + Math.sin(camera.rotation.y) * 0.1;
        var valorz = camera.position.z + Math.cos(camera.rotation.y) * 0.1;
        if (!data[Math.round(valorx + epsilon)][Math.round(valorz + epsilon)]) {
            camera.position.x = valorx
            camera.position.z = valorz
        }
    }
    if (keyboard.eventMatches(event, 'left')) {
        camera.rotation.y += 0.1;
    }
    if (keyboard.eventMatches(event, 'right')) {
        camera.rotation.y -= 0.1;
    }
    if (keyboard.eventMatches(event, 'up')) {
        camera.rotation.x += 0.1;
    }
    if (keyboard.eventMatches(event, 'down')) {
        camera.rotation.x -= 0.1;
    }
    if (keyboard.eventMatches(event, 'space')) {
        cameraControls = new THREE.OrbitControls(camera);
        cameraControls.nokeys = true
        camera.position.y += 3
        cameraControlsActivado = true
    }
    if (keyboard.eventMatches(event, 'r')) {
        location.reload();
    }
})



