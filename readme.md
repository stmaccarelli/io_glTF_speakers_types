#glTF extras: Speakers and Blender Object Types addon#


This addon  exports Speakers data and Blender Object types into extra fields of a glTF.
extras are custom fields you can write into the glTF. They will mean nothing for a official, standard glTF importer.
To actually make use of those data, a parsing function must be coded in the importer, I'll provide a sample method for [three.js](https://github.com/mrdoob/three.js), that's the environment this addon was built for.

THOSE ARE NOT NATIVE glTF FUNCTIONALITIES, NOR THIS ADDON WILL ADD ANY FUNCTIONALITY TO glTF FILE FORMAT

---

##Blender Scene

the audio file will not be embedded in the glTF, and must be placed in the same folder of the glTF file.
.. figure:: https://code.blender.org/wp-content/uploads/2018/12/springrg.jpg
   :scale: 50 %
   :align: center

---

##The Exporter

---

##three.js sample parse code for Speakers

_the audio file will not be embedded in the glTF, and must be placed in the webserver. This sample code assumes it's in the same folder of the glTF file._


```javascript
new GLTFLoader().load( "./glTF-file.glb", function ( gltf ) {

    scene.add( gltf.scene );

    gltf.scene.traverse( function ( child ) {
            
        if ( child.userData.type && child.userData.type == "SPEAKER" ){

            // the Speaker children, is an empty object in three.js, with no geometry nor material
            // this is needed in case you'll use a PositionalAudio helper
            child.rotateX(Math.PI / 2);

            // an audioLoader must be previously created
            audioLoader.load( child.userData.filename, function( buffer ) {

                // an audioListener must be previously created

                // create the PositionalAudio object (passing in the listener)
                let sound = new THREE.PositionalAudio( audioListener );

                sound.setBuffer( buffer );                
                sound.setVolume( child.userData.volume );
                sound.setPlaybackRate( child.userData.pitch );

                sound.setRefDistance( child.userData.distance_reference );
                sound.setMaxDistance( child.userData.distance_max );

                sound.setDirectionalCone(
                    child.userData.cone_angle_inner,
                    child.userData.cone_angle_outer,
                    child.userData.cone_volume_outer
                );

                sound.setLoop( true );
                sound.play();
                            
                child.add( sound );
            });
        }
    
    })
});

```
---

##Final result







##License
-------

As Blender, this addon is licensed under the GNU General Public License, Version 3.

See [blender.org/about/license](https://www.blender.org/about/license) for details.