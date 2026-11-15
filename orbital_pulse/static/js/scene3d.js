/**
 * ORBITAL PULSE - 3D Spacecraft Builder & Orbital Globe Simulator
 * Section 8: Interactive 3D Spacecraft & Trajectory Globe
 * Uses Three.js WebGL with procedural geometry and orbit visualizer.
 */

class SpacecraftScene3D {
  constructor(canvasContainerId) {
    this.container = document.getElementById(canvasContainerId);
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.spacecraftGroup = null;
    this.orbitGroup = null;
    this.planetMesh = null;
    this.atmosphereMesh = null;
    this.orbitLine = null;
    this.satelliteMarker = null;

    this.mode = 'spacecraft'; // 'spacecraft' or 'orbit'
    this.level = 1;
    this.simAngle = 0;
    this.rotationSpeed = 0.005;

    // Component meshes attached to spacecraft
    this.attachedMeshes = {
      bus: null,
      solarWings: null,
      instruments: null,
      antenna: null,
      engine: null
    };

    this.init();
  }

  init() {
    if (!this.container) return;

    const width = this.container.clientWidth || 600;
    const height = this.container.clientHeight || 400;

    // 1. Three.js Scene Setup
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x070b14, 0.0015);

    // 2. Camera Setup
    this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    this.camera.position.set(0, 5, 12);
    this.camera.lookAt(0, 0, 0);

    // 3. Renderer Setup
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(window.devicePixelRatio || 1);
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.container.appendChild(this.renderer.domElement);

    // 4. Lighting Setup
    const ambientLight = new THREE.AmbientLight(0x223344, 1.2);
    this.scene.add(ambientLight);

    this.sunLight = new THREE.DirectionalLight(0xffffff, 2.8);
    this.sunLight.position.set(20, 10, 15);
    this.scene.add(this.sunLight);

    const blueRimLight = new THREE.PointLight(0x00f0ff, 1.5, 50);
    blueRimLight.position.set(-15, -10, -10);
    this.scene.add(blueRimLight);

    // 5. Starfield Background
    this.createStarfield();

    // 6. Build Spacecraft Modular Group
    this.spacecraftGroup = new THREE.Group();
    this.scene.add(this.spacecraftGroup);

    // 7. Build Orbit & Celestial Group
    this.orbitGroup = new THREE.Group();
    this.orbitGroup.visible = false;
    this.scene.add(this.orbitGroup);

    this.buildDefaultBus(1);

    // Mouse Interaction / Orbit Controls
    this.setupInteraction();

    // Window resize handler
    window.addEventListener('resize', () => this.onResize());

    // Animation Loop
    this.animate();
  }

  createStarfield() {
    const starCount = 800;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(starCount * 3);
    const colors = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 400;
      positions[i + 1] = (Math.random() - 0.5) * 400;
      positions[i + 2] = (Math.random() - 0.5) * 400;

      const shade = Math.random() * 0.5 + 0.5;
      colors[i] = shade * 0.8;
      colors[i + 1] = shade * 0.9;
      colors[i + 2] = shade;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 1.2,
      vertexColors: true,
      transparent: true,
      opacity: 0.85
    });

    const starPoints = new THREE.Points(geometry, material);
    this.scene.add(starPoints);
  }

  buildDefaultBus(level = 1) {
    this.level = level;
    // Clear existing meshes
    while (this.spacecraftGroup.children.length > 0) {
      this.spacecraftGroup.remove(this.spacecraftGroup.children[0]);
    }

    // Main Chassis
    let busGeom;
    if (level === 1) {
      // 6U CubeSat Chassis (10 x 20 x 30 cm proportions)
      busGeom = new THREE.BoxGeometry(1.2, 2.4, 3.6);
    } else if (level === 2) {
      // JWST style Hexagonal Bus
      busGeom = new THREE.CylinderGeometry(2.0, 2.4, 1.8, 6);
    } else if (level === 3) {
      // Lunar lander chassis
      busGeom = new THREE.CylinderGeometry(2.2, 2.8, 2.0, 8);
    } else if (level === 4) {
      // Gateway Crew Module
      busGeom = new THREE.CylinderGeometry(2.2, 2.2, 5.0, 16);
    } else {
      // Deep Space Interplanetary Spine
      busGeom = new THREE.CylinderGeometry(1.8, 1.8, 8.0, 16);
    }

    const busMat = new THREE.MeshStandardMaterial({
      color: 0xd4af37, // Gold MLI Foil
      metalness: 0.85,
      roughness: 0.25
    });

    const busMesh = new THREE.Mesh(busGeom, busMat);
    this.spacecraftGroup.add(busMesh);
    this.attachedMeshes.bus = busMesh;

    // Accent framework
    const frameGeom = new THREE.BoxGeometry(1.25, 2.45, 3.65);
    const frameMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.3 });
    const wireMesh = new THREE.Mesh(frameGeom, frameMat);
    this.spacecraftGroup.add(wireMesh);
  }

  updateModularComponents(selectedComponents, level = 1) {
    this.level = level;

    // Reset attachments
    if (this.attachedMeshes.solarWings) {
      this.spacecraftGroup.remove(this.attachedMeshes.solarWings);
      this.attachedMeshes.solarWings = null;
    }
    if (this.attachedMeshes.instruments) {
      this.spacecraftGroup.remove(this.attachedMeshes.instruments);
      this.attachedMeshes.instruments = null;
    }
    if (this.attachedMeshes.antenna) {
      this.spacecraftGroup.remove(this.attachedMeshes.antenna);
      this.attachedMeshes.antenna = null;
    }
    if (this.attachedMeshes.engine) {
      this.spacecraftGroup.remove(this.attachedMeshes.engine);
      this.attachedMeshes.engine = null;
    }

    const st2 = selectedComponents['station_2'];
    const st3 = selectedComponents['station_3'];
    const st4 = selectedComponents['station_4'];

    // 1. Solar Wings / Power
    if (st2 && st2.id === 'pwr_deployable_wings') {
      const wingsGroup = new THREE.Group();
      const wingGeom = new THREE.BoxGeometry(3.5, 1.2, 0.08);
      const wingMat = new THREE.MeshStandardMaterial({
        color: 0x1e3a8a, // Deep blue solar cell
        metalness: 0.5,
        roughness: 0.2
      });

      const leftWing = new THREE.Mesh(wingGeom, wingMat);
      leftWing.position.set(-2.8, 0, 0);
      const rightWing = new THREE.Mesh(wingGeom, wingMat);
      rightWing.position.set(2.8, 0, 0);

      wingsGroup.add(leftWing);
      wingsGroup.add(rightWing);
      this.spacecraftGroup.add(wingsGroup);
      this.attachedMeshes.solarWings = wingsGroup;
    } else if (st2 && st2.id === 'therm_cryocooler_5layer') {
      // 5-Layer Sunshield
      const shieldGroup = new THREE.Group();
      const shieldGeom = new THREE.BoxGeometry(9.0, 0.2, 5.5);
      const shieldMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.9, roughness: 0.1 });
      const shield = new THREE.Mesh(shieldGeom, shieldMat);
      shield.position.set(0, -1.2, 0);
      shieldGroup.add(shield);
      this.spacecraftGroup.add(shieldGroup);
      this.attachedMeshes.solarWings = shieldGroup;
    }

    // 2. Science / Bio Payload
    if (st3) {
      const payloadGroup = new THREE.Group();
      if (st3.id === 'pay_bio_incubator') {
        // Glowing Bio-Incubator Pod
        const podGeom = new THREE.CylinderGeometry(0.5, 0.5, 1.2, 12);
        const podMat = new THREE.MeshStandardMaterial({ color: 0x10b981, emissive: 0x059669, emissiveIntensity: 0.6 });
        const pod = new THREE.Mesh(podGeom, podMat);
        pod.position.set(0, 0, 1.8);
        payloadGroup.add(pod);
      } else if (st3.id === 'pay_lunar_drill_isru') {
        // Rotary Core Drill assembly
        const drillGeom = new THREE.CylinderGeometry(0.15, 0.08, 3.2, 8);
        const drillMat = new THREE.MeshStandardMaterial({ color: 0xcccccc, metalness: 0.95 });
        const drill = new THREE.Mesh(drillGeom, drillMat);
        drill.position.set(0, -2.2, 0);
        payloadGroup.add(drill);
      } else if (st3.id === 'bio_trauma_pod_eclss') {
        // Medical Trauma Module
        const traumaGeom = new THREE.BoxGeometry(2.4, 1.8, 2.2);
        const traumaMat = new THREE.MeshStandardMaterial({ color: 0xef4444, emissive: 0x991b1b, emissiveIntensity: 0.4 });
        const trauma = new THREE.Mesh(traumaGeom, traumaMat);
        trauma.position.set(0, 0, 2.5);
        payloadGroup.add(trauma);
      }
      this.spacecraftGroup.add(payloadGroup);
      this.attachedMeshes.instruments = payloadGroup;
    }

    // 3. Comms / Antennas
    if (st4) {
      const commsGroup = new THREE.Group();
      if (st4.id === 'comms_sband_patch') {
        const patchGeom = new THREE.BoxGeometry(0.8, 0.8, 0.1);
        const patchMat = new THREE.MeshStandardMaterial({ color: 0xffffff });
        const patch = new THREE.Mesh(patchGeom, patchMat);
        patch.position.set(0, 1.3, 0);
        commsGroup.add(patch);
      } else if (st4.id === 'comms_kaband_deepspace' || st4.id === 'comms_laser_dsoc') {
        // Parabolic Dish / Laser Terminal
        const dishGeom = new THREE.CylinderGeometry(1.6, 0.2, 0.4, 24, 1, true);
        const dishMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, metalness: 0.7, side: THREE.DoubleSide });
        const dish = new THREE.Mesh(dishGeom, dishMat);
        dish.rotation.x = Math.PI / 4;
        dish.position.set(0, 1.8, 0);
        commsGroup.add(dish);
      }
      this.spacecraftGroup.add(commsGroup);
      this.attachedMeshes.antenna = commsGroup;
    }
  }

  switchToOrbitView(level = 1) {
    this.mode = 'orbit';
    this.spacecraftGroup.visible = false;
    this.orbitGroup.visible = true;

    // Clear previous orbit objects
    while (this.orbitGroup.children.length > 0) {
      this.orbitGroup.remove(this.orbitGroup.children[0]);
    }

    // Build Central Celestial Body
    let bodyRadius = 3.5;
    let bodyColor = 0x1d4ed8; // Earth blue

    if (level === 3 || level === 4) {
      bodyRadius = 2.8;
      bodyColor = 0x94a3b8; // Moon grey
    } else if (level === 5) {
      bodyRadius = 1.6;
      bodyColor = 0x78716c; // Asteroid metallic brown
    }

    const sphereGeom = new THREE.SphereGeometry(bodyRadius, 32, 32);
    const sphereMat = new THREE.MeshStandardMaterial({
      color: bodyColor,
      roughness: 0.7,
      metalness: 0.1
    });

    this.planetMesh = new THREE.Mesh(sphereGeom, sphereMat);
    this.orbitGroup.add(this.planetMesh);

    // Orbit Ring
    const orbitRadius = bodyRadius * 1.85;
    const points = [];
    const segments = 64;
    for (let i = 0; i <= segments; i++) {
      const theta = (i / segments) * Math.PI * 2;
      points.push(new THREE.Vector3(Math.cos(theta) * orbitRadius, Math.sin(theta) * (orbitRadius * 0.4), Math.sin(theta) * orbitRadius));
    }
    const orbitGeom = new THREE.BufferGeometry().setFromPoints(points);
    const orbitMat = new THREE.LineBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.75 });
    this.orbitLine = new THREE.Line(orbitGeom, orbitMat);
    this.orbitGroup.add(this.orbitLine);

    // Satellite Dot
    const satGeom = new THREE.SphereGeometry(0.25, 12, 12);
    const satMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
    this.satelliteMarker = new THREE.Mesh(satGeom, satMat);
    this.orbitGroup.add(this.satelliteMarker);

    this.camera.position.set(0, 8, 16);
    this.camera.lookAt(0, 0, 0);
  }

  switchToSpacecraftView() {
    this.mode = 'spacecraft';
    this.spacecraftGroup.visible = true;
    this.orbitGroup.visible = false;
    this.camera.position.set(0, 5, 12);
    this.camera.lookAt(0, 0, 0);
  }

  setupInteraction() {
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;

    const el = this.renderer.domElement;

    el.addEventListener('mousedown', (e) => {
      isDragging = true;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    });

    window.addEventListener('mouseup', () => {
      isDragging = false;
    });

    el.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMouseX;
      const deltaY = e.clientY - prevMouseY;

      if (this.mode === 'spacecraft') {
        this.spacecraftGroup.rotation.y += deltaX * 0.008;
        this.spacecraftGroup.rotation.x += deltaY * 0.008;
      } else {
        this.orbitGroup.rotation.y += deltaX * 0.008;
        this.orbitGroup.rotation.x += deltaY * 0.008;
      }

      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    });

    el.addEventListener('wheel', (e) => {
      this.camera.position.z = Math.max(5, Math.min(35, this.camera.position.z + e.deltaY * 0.02));
    });
  }

  onResize() {
    if (!this.container || !this.renderer || !this.camera) return;
    const width = this.container.clientWidth;
    const height = this.container.clientHeight;
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    if (this.mode === 'spacecraft') {
      this.spacecraftGroup.rotation.y += this.rotationSpeed;
    } else if (this.mode === 'orbit' && this.satelliteMarker) {
      this.simAngle += 0.02;
      const bodyRadius = this.level >= 3 ? (this.level === 5 ? 1.6 : 2.8) : 3.5;
      const orbitRadius = bodyRadius * 1.85;

      this.satelliteMarker.position.x = Math.cos(this.simAngle) * orbitRadius;
      this.satelliteMarker.position.y = Math.sin(this.simAngle) * (orbitRadius * 0.4);
      this.satelliteMarker.position.z = Math.sin(this.simAngle) * orbitRadius;

      if (this.planetMesh) {
        this.planetMesh.rotation.y += 0.002;
      }
    }

    this.renderer.render(this.scene, this.camera);
  }
}
