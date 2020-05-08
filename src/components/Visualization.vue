<template>
    <div class="vis">
        <img src='@/assets/iris-sample.png'>
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
        <canvas id="main-canvas"></canvas>
    </div>
</template>

<script>
export default {
    name: 'Annotation',
    props: {}
}
</script>

<style scoped>
.vis {
    background-color: #fff;
}
#main-canvas {
    width: 500px;
    height: 300px;
}
#control-panel {
    background: #eee;
    border-radius: 1em;
    padding: 1em;
}
</style>
