<template>
    <div class="vis">
        <Canvas></Canvas>
        <div id="control-panel">
            <h3>Controls</h3>
            <ul>
                <li id="btn-previous">Previous</li>
                <li id="btn-next">Next</li>
                <li id="btn-undo">Undo</li>
                <li id="btn-redo">Redo</li>
                <li id="btn-brush">Brush</li>
                <li id="btn-eraser">Eraser</li>
            </ul>
        </div>
    </div>
</template>

<script>
import Canvas from '@/components/Canvas'

export default {
    name: 'Annotation',
    components: { Canvas },
    props: {},
}
</script>

<style scoped>
.vis {
    background-color: #fff;
}
#control-panel {
    background: #eee;
    border-radius: 1em;
    padding: 1em;
}
</style>
