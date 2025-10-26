import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

const ThreeJSViewer = ({ modelData, style = {} }) => {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const animationRef = useRef(null);

  useEffect(() => {
    if (!mountRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB); // Sky blue
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth > 768 ? 16/9 : 4/3, 0.1, 1000);
    camera.position.set(10, 8, 10);
    camera.lookAt(0, 0, 0);

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    const width = mountRef.current.clientWidth || 800;
    const height = mountRef.current.clientHeight || 500;
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    rendererRef.current = renderer;

    // Clear any existing content
    while (mountRef.current.firstChild) {
      mountRef.current.removeChild(mountRef.current.firstChild);
    }
    mountRef.current.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    // Materials
    const materials = {
      foundation: new THREE.MeshLambertMaterial({ color: 0x8B4513 }),
      wall: new THREE.MeshLambertMaterial({ color: 0xD2B48C }),
      roof_traditional: new THREE.MeshLambertMaterial({ color: 0xDC143C }),
      roof_modern: new THREE.MeshLambertMaterial({ color: 0x708090 }),
      window: new THREE.MeshLambertMaterial({ color: 0x87CEEB, transparent: true, opacity: 0.8 }),
      door: new THREE.MeshLambertMaterial({ color: 0x8B4513 }),
    };

    // Create house based on model data or default
    if (modelData && modelData.objects && modelData.objects.length > 0) {
      modelData.objects.forEach(obj => {
        let geometry;
        
        switch (obj.type) {
          case 'box':
            geometry = new THREE.BoxGeometry(
              obj.dimensions?.width || 1,
              obj.dimensions?.height || 1,
              obj.dimensions?.depth || 1
            );
            break;
          case 'sphere':
            geometry = new THREE.SphereGeometry(obj.radius || 0.5, 32, 32);
            break;
          case 'cylinder':
            geometry = new THREE.CylinderGeometry(
              obj.radiusTop || 0.5,
              obj.radiusBottom || 0.5,
              obj.height || 1,
              32
            );
            break;
          default:
            geometry = new THREE.BoxGeometry(1, 1, 1);
        }

        const material = materials[obj.material] || materials.wall;
        const mesh = new THREE.Mesh(geometry, material);
        
        if (obj.position) {
          mesh.position.set(obj.position.x || 0, obj.position.y || 0, obj.position.z || 0);
        }
        
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        scene.add(mesh);
      });
    } else {
      // Create default house
      createDefaultHouse(scene, materials);
    }

    // Ground
    const groundGeometry = new THREE.PlaneGeometry(20, 20);
    const groundMaterial = new THREE.MeshLambertMaterial({ color: 0x90EE90 });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.1;
    ground.receiveShadow = true;
    scene.add(ground);

    // Animation
    const animate = () => {
      animationRef.current = requestAnimationFrame(animate);
      
      const time = Date.now() * 0.001;
      camera.position.x = Math.cos(time * 0.2) * 12;
      camera.position.z = Math.sin(time * 0.2) * 12;
      camera.lookAt(0, 2, 0);
      
      renderer.render(scene, camera);
    };

    animate();

    // Cleanup
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      
      renderer.dispose();
    };
  }, [modelData]);

  const createDefaultHouse = (scene, materials) => {
    // Main house
    const houseGeometry = new THREE.BoxGeometry(4, 3, 4);
    const house = new THREE.Mesh(houseGeometry, materials.wall);
    house.position.y = 1.5;
    house.castShadow = true;
    house.receiveShadow = true;
    scene.add(house);

    // Roof
    const roofGeometry = new THREE.ConeGeometry(3, 1.5, 4);
    const roof = new THREE.Mesh(roofGeometry, materials.roof_traditional);
    roof.position.y = 3.75;
    roof.rotation.y = Math.PI / 4;
    roof.castShadow = true;
    scene.add(roof);

    // Door
    const doorGeometry = new THREE.BoxGeometry(0.8, 2, 0.1);
    const door = new THREE.Mesh(doorGeometry, materials.door);
    door.position.set(0, 1, 2.05);
    door.castShadow = true;
    scene.add(door);

    // Windows
    const windowGeometry = new THREE.BoxGeometry(1, 1, 0.1);
    
    const window1 = new THREE.Mesh(windowGeometry, materials.window);
    window1.position.set(-1.5, 2, 2.05);
    scene.add(window1);
    
    const window2 = new THREE.Mesh(windowGeometry, materials.window);
    window2.position.set(1.5, 2, 2.05);
    scene.add(window2);
  };

  return (
    <div 
      ref={mountRef} 
      style={{
        width: '100%',
        height: '500px',
        minHeight: '400px',
        border: '2px solid rgba(255, 255, 255, 0.3)',
        borderRadius: '20px',
        overflow: 'hidden',
        backgroundColor: '#f0f8ff',
        boxShadow: '0 20px 60px rgba(0, 0, 0, 0.15)',
        backdropFilter: 'blur(10px)',
        ...style
      }}
    />
  );
};

export default ThreeJSViewer;