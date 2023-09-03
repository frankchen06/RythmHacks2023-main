<template>
    <div v-if="queue?.[0] != undefined" class="relative order-2">
        <div v-for="item in queue.slice().reverse()" :key="Math.random()" :style="`transform: translate(${item.x}px, ${item.y}px) rotate(${item.rot}deg);`" class="rounded-2xl shadow-2xl absolute w-full h-full border-cool">
            <div :style="`transform: scaleX(0.9) scaleY(0.94); background-image: url(${item.image_url});`" class="card absolute bg-black w-full h-full rounded-2xl">
            </div>
        </div>
    </div>
    <div v-if="queue?.[0] == undefined" class="w-full h-full bg-grey order-2">
        <MainLoader></MainLoader>
    </div>
</template>

<script>
import MainLoader from './MainLoader.vue';

export default {
    name: "MainStack",
    props: {
        queue: null
    },
    components: {
        MainLoader,
    },
}
</script>

<style scoped>
    .card {
        background-repeat: no-repeat;
        background: linear-gradient(1turn, pink, lightgreen);
        background-size: cover;
        background-position: 50%;
    }

</style>