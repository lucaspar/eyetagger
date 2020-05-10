<template>
    <div class="section ann">
        <Canvas></Canvas>
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
.ann {
    background-color: #fff;
    padding-top: 0;
}
#control-panel {
    background: #eee;
    border-radius: 1em;
    padding: 1em;
}
</style>
