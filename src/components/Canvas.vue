<template>
    <div ref='cnv' class="cnv section columns is-multiline" @keyup.left="prev_image" @keyup.81="prev_image" @keyup.right="next_image" @keyup.69="next_image">
        <div v-if="imgID_short" class="image_id">
            <small>ID: {{ imgID_short }}</small>
        </div>
        <div class="center column is-full">
            <h4 class="title is-4 has-text-centered">Iris #{{ this.sequential_counter + 1 }}</h4>
        </div>
        <div class="column is-full">
            <div class="columns is-multiline is-centered">
                <div class="column is-2" id="control-panel">
                    <div class="columns is-multiline">
                        <div class="column is-6"><button class="button is-info" id="btn-previous"   @click="prev_image"> <b-icon pack="fas" icon="chevron-left">     </b-icon> <span>Previous (Q)</span> </button>   </div>
                        <div class="column is-6"><button class="button is-info" id="btn-next"       @click="next_image"> <b-icon pack="fas" icon="chevron-right">    </b-icon> <span>Next (E)</span>     </button>   </div>
                        <div class="column is-6"><button class="button is-info" id="btn-undo">       <b-icon pack="fas" icon="undo">        </b-icon> <span>Undo (Z)</span>     </button>   </div>
                        <div class="column is-6"><button class="button is-info" id="btn-redo">       <b-icon pack="fas" icon="redo">        </b-icon> <span>Redo (X)</span>     </button>   </div>
                        <div class="column is-6 is-offset-3"><button class="button is-info" id="btn-brush"> <b-icon pack="fas" icon="brush">       </b-icon> <span>Brush</span>    </button>   </div>
                        <hr>
                        <div class="column is-6 is-offset-3"><button class="button is-success" id="btn-save" @click="export_annotation"> <b-icon pack="fas" icon="save">            </b-icon> <span>Export</span>    </button>   </div>
                        <!-- <div class="column is-6"><button class="button is-info" id="btn-eraser">     <b-icon pack="fas" icon="eraser">           </b-icon> <span>Eraser</span>   </button>   </div> -->
                    </div>
                </div>
                <div class="column">
                    <canvas id="vis-canvas" ref="vis-canvas"/>
                </div>
                <div class="column">
                    <canvas id="main-canvas" ref="main-canvas"/>
                </div>
                <div class="column">
                    <canvas class="hidden" id="export-canvas" ref="export-canvas"></canvas>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { fabric } from 'fabric'
import { mapState } from 'vuex'

export default {
    name: 'Canvas',
    props: {},
    data() {
        return {
            // the CanvasRenderingContext to turn canvas into a reactive component:
            paths_group: new fabric.Group(),
            context: null,
            image: null,
        }
    },
    computed: {
        ...mapState('images', [
            'images',
            'annotations',
            'sequential_counter',
            'canvas_image',
        ]),
        imgID_short: function() {
            if (this.canvas_image && this.canvas_image.imgID) {
                return this.canvas_image.imgID.substr(this.canvas_image.imgID.length - 10)
            }
            return undefined
        },
        comp_annotations() {
            console.log(this.images)
            if (this.images && this.images.annotations) {
                console.log(this.images.annotations.length)
                return this.images.annotations
            }
            return {}
        },
    },
    methods: {

        prev_image: function() {
            this.export_annotation()
            this.$store.dispatch('images/decSeqCounter')
        },

        next_image: function() {
            if (this.annotations) {
                console.log(typeof this.annotations)
                console.log("AAA", Object.values(this.annotations).length);
            }
            this.export_annotation()
            this.$store.dispatch('images/incSeqCounter')
        },

        post_annotations: function() {
            console.log('POSTING ANNOTATIONS');
            this.$store.dispatch('images/postAnnotations')
        },

        canvas_clear: function() {
            this.canvas.main_canvas.getObjects().map( o => {
                this.canvas.main_canvas.remove(o)
            })
        },

        export_annotation: function() {
            console.log('Exporting annotation');

            // other useful methods:
            // console.log(this.canvas.main_canvas.toSVG())
            // console.log(this.canvas.main_canvas.toObject())

            // clone objects from main-canvas, as we cannot directly
            // export tainted canvases due to security constraints
            this.canvas.main_canvas.getObjects()
                .map(o => this.canvas.export_canvas.add(o))
            this.canvas.export_canvas.renderAll()

            // convert canvas to image
            this.$refs['export-canvas'].toBlob( blob => {

                // now objects can be removed from export canvas
                this.canvas.export_canvas.getObjects().map( o => {
                    this.canvas.export_canvas.remove(o)
                })

                // display generated image (optional)
                const new_img = document.createElement('img'),
                    url = URL.createObjectURL(blob);
                new_img.onload = function() {
                    URL.revokeObjectURL(url);
                };
                new_img.src = url;
                document.body.appendChild(new_img);

                // convert blob to base64 for later upload
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                reader.onloadend = () => {
                    const base64data = reader.result;
                    const payload = {
                        imgID: this.canvas_image.imgID,
                        annotation: base64data,
                    }
                    this.$store.dispatch('images/setAnnotation', payload)
                }
            })

        },

        update_canvas_image: function() {

            // need both counter and list of images to update canvas image
            if (this.sequential_counter == undefined ||
                this.images == undefined ||
                this.images.length <= this.sequential_counter + 1) {
                return
            }
            let canvas_image = this.images[this.sequential_counter]
            this.$store.dispatch('images/setCanvasImage', canvas_image)
        },

        update_canvas_display: function() {

            // if there's no image to show, there's nothing else to do
            if (this.canvas_image == undefined || !this.canvas_image.imgID) {
                return
            }

            // set canvas references
            const canvas = this.$refs['main-canvas']
            this.canvas = this.canvas ? this.canvas : {}
            this.canvas.main_canvas = this.canvas.main_canvas ?
                this.canvas.main_canvas :
                new fabric.Canvas(canvas)
            this.canvas.vis_canvas = this.canvas.vis_canvas ?
                this.canvas.vis_canvas :
                new fabric.Canvas(this.$refs['vis-canvas'])
            this.canvas.export_canvas = this.canvas.export_canvas ?
                this.canvas.export_canvas :
                new fabric.Canvas(this.$refs['export-canvas'])
            // this.context = canvas.getContext('2d')

            // set up iris image
            if (!this.image) {
                this.image = new window.Image()
            }
            this.canvas_image_source = process.env.VUE_APP_DATASET_ROOT + this.canvas_image.imgStaticPath
            this.image.src = "";
            this.image.src = this.canvas_image_source
            this.image.crossOrigin = "Anonymous";
            this.image.onerror = () => {
                console.error("Image not found:", this.image.src);
            }
            this.image.onload = () => {

                console.log("LOADED:", this.canvas_image_source);

                // remove old objects from main_canvas
<<<<<<< HEAD
                this.canvas_clear()
=======
                this.canvas.main_canvas.getObjects().map( o => {
                    this.canvas.main_canvas.remove(o)
                })
>>>>>>> f4c950cc1eaac7b1828cc9c3e1c3480ec0bedc7f

                // prepare visualization canvas
                this.canvas.vis_canvas.isDrawingMode = false
                this.canvas.vis_canvas.setBackgroundImage(this.canvas_image_source, this.canvas.vis_canvas.renderAll.bind(this.canvas.vis_canvas))
                this.canvas.vis_canvas.setDimensions({ width: this.image.naturalWidth, height: this.image.naturalHeight })
                // this.canvas.vis_canvas.renderAll();

                // prepare main canvas
                this.canvas.main_canvas.isDrawingMode = true
                this.canvas.main_canvas.setBackgroundImage(this.canvas_image_source, this.canvas.main_canvas.renderAll.bind(this.canvas.main_canvas))
                this.canvas.main_canvas.setDimensions({ width: this.image.naturalWidth, height: this.image.naturalHeight })
                this.canvas.main_canvas.renderAll();

                // prepare export canvas
                this.canvas.export_canvas.setDimensions({width: this.image.naturalWidth, height: this.image.naturalHeight })

                // set brush properties
                this.canvas.main_canvas.freeDrawingBrush.width = 20
                this.canvas.main_canvas.freeDrawingBrush.color = "#f005"

            }

            this.canvas.main_canvas.on('mouse:up', () => {

                // disolve existing group
                this.paths_group._restoreObjectsState()
                this.canvas.main_canvas.remove(this.paths_group)

                // select all objects for re-grouping
                const objs = this.canvas.main_canvas.getObjects().map( o => o.set('active', true) )
                this.paths_group = new fabric.Group(objs, {
                    originX: 'center',
                    originY: 'center',
                })
                const items = this.canvas.main_canvas.getObjects()
                console.log("Objects in this annotation:", items.length);

                // cloning an object
                // const new_item = fabric.util.object.clone(items[items.length-1])
                // new_item.set("top", new_item.top + 5)
                // new_item.set("left", new_item.left + 5)
                // new_item.set("fill", "#0f0");
                // this.canvas.main_canvas.add(new_item)

            })

        }

    },  // end of 'methods'
    watch: {

        // update canvas image when image array changes
        images: {
            handler: 'update_canvas_image',
        },

        // update canvas image when sequential counter changes
        sequential_counter: {
            handler: 'update_canvas_image',
        },

        // update displayed image when canvas image changes
        canvas_image: {
            handler: 'update_canvas_display',
        },

        // post annotations to server when they change
        annotations: {
            handler: 'post_annotations',
            deep: true,
        },

    },  // end of 'watch'
    mounted() {
        this.$refs['cnv'].focus()
        if (this.annotations) {
            console.log(typeof this.annotations)
            console.log("AAA", Object.values(this.annotations).length);
        }
        this.update_canvas_image()
        this.update_canvas_display()
    },
}
</script>

<style scoped>
#main-canvas {
    width: 100%;
    height: 100%;
    display: block;
    margin: auto;
    border: 1px solid #09f;
    border-radius: 0.5em;
}
.image_id {
    font-family: 'Courier New', Courier, monospace;
    text-align: right;
    position: absolute;
    font-size: 9pt;
    color: #888;
    margin: 1em;
    right: 0;
    top: 0;
}
button {
    width: 100%;
}
.cnv {
    padding-top: 0;
}
.hidden {
    border: 1px solid red;
    /* display: none; */
}
</style>
