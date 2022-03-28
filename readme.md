glTF extras: Speakers and Blender Object Types addon
===

This addon exports Speakers data and Blender Object types into extra fields of a glTF.
extras are custom fields you can write into the glTF. They will mean nothing for a official, standard glTF importer.
To actually make use of those data, a parsing function must be coded in the importer, I'll provide a sample method for [three.js](https://github.com/mrdoob/three.js), that's the environment this addon was built for.

THOSE ARE NOT NATIVE glTF FUNCTIONALITIES, NOR THIS ADDON WILL ADD ANY FUNCTIONALITY TO glTF FILE FORMAT

This addon can also export Blender objects types names as extra fields in the glTF file. This may be useful to distinguish between placeholder objects, or whatever use you may think of.


Installation
---
Install this addon from Blender Preferences > Addons > Install... > Select the file, load it > activate the addon by checking it.

Blender Scene
---
Load the audio file and set the Speaker as you'd normally do in Blender.
The audio file will not be embedded in the glTF.

<img width="1264" alt="Blender scene" src="https://user-images.githubusercontent.com/1394193/160487465-dcefc757-3cdf-4e08-8c3a-74b1adfb0843.png">


The Exporter
---
The addon is enabled by default, and in the glTF Export window you can disable it.

<img width="1227" alt="Blender glTF Exporter + addons" src="https://user-images.githubusercontent.com/1394193/160486260-5aa42bac-8f5c-4f4a-a9a7-81581a8399fa.png">


three.js sample parse code for Speakers
---
_NOTE: the audio file will not be embedded in the glTF, and must be placed in the webserver. This sample code assumes it's in the same folder of the glTF file._

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


Working Example
---
Using three.js Positional Audio helper to show the speaker position and cone.

https://user-images.githubusercontent.com/1394193/160486554-f5ea958f-1305-4f52-8f9c-12d28f37097f.mp4


License
---

As a Blender addon, this addon is licensed under the GNU General Public License, Version 3.

See [blender.org/about/license](https://www.blender.org/about/license) for details.
