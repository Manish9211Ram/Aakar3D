import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

const ThreeJSViewer = ({ modelData, width = 600, height = 400 }) => {
  const mountRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const animationRef = useRef(null);

  useEffect(() => {
    if (!modelData) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB); // Sky blue background
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(
      75,
      width / height,
      0.1,
      1000
    );
    
    const cameraData = modelData.camera || { position: [15, -15, 10], target: [0, 0, 3] };
    camera.position.set(...cameraData.position);
    camera.lookAt(new THREE.Vector3(...cameraData.target));

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    rendererRef.current = renderer;

    // Clear any existing content
    if (mountRef.current) {
      mountRef.current.innerHTML = '';
      mountRef.current.appendChild(renderer.domElement);
    }

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    const lightData = modelData.lighting?.sun || { position: [10, 10, 20] };
    directionalLight.position.set(...lightData.position);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    // Materials
    const materials = {
      foundation: new THREE.MeshLambertMaterial({ color: 0x8B4513 }),
      wall: new THREE.MeshLambertMaterial({ color: 0xD2B48C }),
      roof_traditional: new THREE.MeshLambertMaterial({ color: 0xDC143C }),
      roof_modern: new THREE.MeshLambertMaterial({ color: 0x708090 }),
      roof_rajasthani: new THREE.MeshLambertMaterial({ color: 0xCD853F }),
      window: new THREE.MeshLambertMaterial({ color: 0x87CEEB, transparent: true, opacity: 0.8 }),
      door: new THREE.MeshLambertMaterial({ color: 0x8B4513 }),
      door_frame: new THREE.MeshLambertMaterial({ color: 0x654321 }),
      balcony: new THREE.MeshLambertMaterial({ color: 0xD2B48C }),
      railing: new THREE.MeshLambertMaterial({ color: 0x8B4513 }),
      roof_detail: new THREE.MeshLambertMaterial({ color: 0xB22222 }),
      dome: new THREE.MeshLambertMaterial({ color: 0xDAA520 }),
      courtyard: new THREE.MeshLambertMaterial({ color: 0xF4A460 }),
      pillar: new THREE.MeshLambertMaterial({ color: 0xD2B48C }),
      tree: new THREE.MeshLambertMaterial({ color: 0x228B22 })
    };

    // Create objects
    modelData.objects?.forEach(obj => {
      let geometry;
      
      if (obj.type === 'box') {
        geometry = new THREE.BoxGeometry(1, 1, 1);
      } else if (obj.type === 'sphere') {
        geometry = new THREE.SphereGeometry(0.5, 16, 12);
      } else if (obj.type === 'cylinder') {
        geometry = new THREE.CylinderGeometry(0.5, 0.5, 1, 12);
      } else if (obj.type === 'pyramid') {
        geometry = new THREE.ConeGeometry(0.7, 1, 4);
      } else {
        geometry = new THREE.BoxGeometry(1, 1, 1); // fallback
      }
      
      const material = materials[obj.material] || new THREE.MeshLambertMaterial({ color: obj.color });
      const mesh = new THREE.Mesh(geometry, material);
      
      // Set position and scale
      mesh.position.set(...obj.position);
      mesh.scale.set(...obj.scale);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      mesh.name = obj.name;
      
      scene.add(mesh);
    });

    // Add ground plane
    const groundGeometry = new THREE.PlaneGeometry(30, 30);
    const groundMaterial = new THREE.MeshLambertMaterial({ color: 0x228B22 });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.5;
    ground.receiveShadow = true;
    scene.add(ground);

    // Animation loop
    const animate = () => {
      animationRef.current = requestAnimationFrame(animate);
      
      // Subtle rotation for the entire scene
      scene.rotation.y += 0.003;
      
      // Special animations for certain objects
      scene.children.forEach(child => {
        if (child.name && child.name.includes('Tree')) {
          // Trees sway gently
          child.rotation.z = Math.sin(Date.now() * 0.001) * 0.1;
        } else if (child.name && child.name.includes('Dome')) {
          // Domes have a subtle glow effect
          child.material.emissive.setHex(0x222222 + Math.sin(Date.now() * 0.005) * 0x111111);
        }
      });
      
      renderer.render(scene, camera);
    };

    animate();

    // Cleanup function
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      
      const currentMount = mountRef.current;
      const currentRenderer = rendererRef.current;
      
      if (currentMount && currentRenderer && currentRenderer.domElement) {
        currentMount.removeChild(currentRenderer.domElement);
      }
      
      if (currentRenderer) {
        currentRenderer.dispose();
      }
    };
  }, [modelData, width, height]);

  return (
    <div 
      ref={mountRef} 
      style={{ 
        width: `${width}px`, 
        height: `${height}px`,
        border: '2px solid rgba(255, 255, 255, 0.3)',
        borderRadius: '8px',
        overflow: 'hidden'
      }} 
    />
  );
};

export default ThreeJSViewer;