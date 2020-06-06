/**
* grafo_sem02.js
* Carga un grafo de escena en Threejs y lo visualiza
*
*/

var render, scene, camera;

var cuboEsfera;
var angulo = 0;

init();
loadScene();
render();

function init() {
    //Inicializar en Threejs

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(new THREE.Color(0x0000AA));
    renderer.shadowMap.enabled = true;
    document.getElementById('container').appendChild(renderer.domElement);

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.set(0.5, 2, 5);
    camera.lookAt(new THREE.Vector3(0, 0, 0));
    var ambiental = new THREE.AmbientLight(0x444444)
    scene.add(ambiental)
    var puntual = new THREE.PointLight("white", 0.2)
    puntual.position.y = 5
    scene.add(puntual)
    var direccional = new THREE.DirectionalLight("white", 0.2)
    direccional.position.set(-2, 3, 10)
    scene.add(direccional)
    var focal = new THREE.SpotLight("white", 0.5)
    focal.position.set(3, 3, -8)
    focal.target.position.set(0, 0, 0)
    focal.angle = Math.PI / 5
    focal.penumbra = 0.5
    focal.castShadow = true;
    scene.add(focal)
}

function loadScene() {
    //Carga la escena
    var mate = new THREE.MeshBasicMaterial({ color: "white", wireframe: false })
    var pulido = new THREE.MeshPhongMaterial({ color: "white", specular: "white", shininess: 1 })

    var geoCubo = new THREE.BoxGeometry(2, 2, 2);
    var matCubo = new THREE.MeshBasicMaterial({ color: 'yellow', wireframe: true });

    var cubo = new THREE.Mesh(geoCubo, mate);
    cubo.receiveShadow = true;
    cubo.castShadow = true;
    cubo.position.set(1.5, 0, 0);
    cubo.add(new THREE.AxesHelper(1));

    var geoEsfera = new THREE.SphereGeometry(0.8, 30, 30);
    var esfera = new THREE.Mesh(geoEsfera, pulido);
    esfera.receiveShadow = true;
    esfera.castShadow = true;
    esfera.position.set(-1.5, 0, 0);

    //Objeto contenedor que no se visualiza ya que no es de tipo malla. Este contendrá al cubo y a la esfera
    cuboEsfera = new THREE.Object3D();
    cuboEsfera.add(cubo);
    cuboEsfera.add(esfera);

    scene.add(cuboEsfera);

    scene.add(new THREE.AxesHelper(3));

    //Suelo
    //var suelo = new THREE.Mesh(new THREE.PlaneGeometry(10, 10, 10, 10), mate)

    //scene.add(suelo)

    //Texto
    var textLoader = new THREE.FontLoader();
    textLoader.load('fonts/helvetiker_regular.typeface.json',
        function (font) {
            var geoText = new THREE.TextGeometry(
                'Guacamole!!',
                {
                    size: 1,
                    height: 0.1,
                    curveSegments: 3,
                    font: font,
                    weight: "bold",
                    style: "normal",
                    bevelThickness: 0.05,
                    bevelSize: 0.04,
                    bevelEnable: true
                })
            var texto = new THREE.Mesh(geoText, matCubo);
            scene.add(texto);
            texto.position.set(-3.5, 2, 0.5);
            //texto.scale.set( 0.5, 0.5, 0.5);
        });

    //Modelo externo
    var loader = new THREE.ObjectLoader();
    loader.load('models/dominos_pizza/case.json',
        function (obj) {
            obj.position.set(0, 1, 0);
            obj.scale.set(2, 2, 2);
            cubo.add(obj);
        });

}

function update() {
    angulo += 0.05;
    cuboEsfera.rotation.y = angulo;
    //cuboEsfera.rotation.z = -angulo;

}

function render() {
    requestAnimationFrame(render);
    update();
    renderer.render(scene, camera);
}