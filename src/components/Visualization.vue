<template>
    <div class="vis">
        <h3>Visualization</h3>
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
