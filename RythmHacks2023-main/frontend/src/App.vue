<script setup>
import MainStack from './components/MainStack.vue'
</script>

<template>
    
    <div class="w-full overflow-hidden">
        <div v-if="!finished" class="grid grid-cols-3 p-8 h-screen">
            <MainStack :queue="queue"></MainStack>
            <div @click="right()" class="flex h-full justify-start items-center order-3">
                <img class="shadow-thing green-arrow" width="200" height="200" src="https://img.icons8.com/stickers/200/arrow.png" alt="arrow"/>
            </div>
            <div @click="left()" class="flex h-full justify-end items-center order-1">
                <img class="shadow-thing red-arrow" width="200" height="200" src="https://img.icons8.com/stickers/200/arrow.png" alt="arrow"/>
            </div>
        </div>
        <div v-if="finished" class="w-full text-center font-sans text-4xl mt-16 text-white text-shadow-md font-bold">
            <h1>Your Style</h1>
        </div>
        <div v-if="finished" class="grid grid-cols-3 gap-4 p-16 h-full">
            <div v-for="item in liked.slice(0,9)" :key="Math.random()">
                <div class="aspect-square w-full rounded image-thing" :style="`background-image: url(${item.image_url}); background-position: center;`" alt="image"></div>
            </div>
        </div>
        <div v-if="finished">
            <div v-if="aiStuff">
                <div class="w-full text-center font-sans text-4xl px-16 text-white text-shadow-md font-bold">
                    <h1 class="mb-4">AI Interpretation</h1>
                    <h3 class="font-normal text-xl text-justify">{{aiStuff.description}}</h3>
                </div>
                <div class="grid grid-cols-2 m-8 gap-8 pb-16">
                    <div class="rounded aspect-square image-thing" :style="`background-image: url(${aiStuff.images[0]})`" alt="image"></div>
                    <div class="rounded aspect-square image-thing" :style="`background-image: url(${aiStuff.images[1]})`" alt="image"></div>
                </div>
            </div>
            <div v-if="!aiStuff" class="relative">
                AI Content is loading...
                <MainLoader></MainLoader>
            </div>
        </div>
    </div>
</template>

<script>
import MainLoader from './components/MainLoader.vue';

export default {
    name:"App",
    data() {
        return {
            queue: null,
            liked: [],
            server: "http://127.0.0.1:5000/",
            maxQueueLength: 30,
            finished: false,
            removeCounter: 0,
            aiStuff: null,
        }
    },
    components: {
        MainLoader,
    },
    async mounted() {
        await this.init()
    },
    methods: {
        left() {
            if (this.queue === null || this.queue.length == 0) {
                if (this.liked.length >= 9 && this.finished != true) {
                    this.finished = true;
                    this.getAIStuff();
                }
                return;
            }
            this.removeCounter++;
            if (this.removeCounter >= 5 && this.liked.length > 0) {
                this.liked.shift();
                this.removeCounter = 0;
            }
            this.queue.shift();
            if (this.queue === null || this.queue.length == 0) {
                if (this.liked.length >= 9  && this.finished != true) {
                    this.finished = true;
                    this.getAIStuff();
                } else {
                    this.queue = null;
                    this.init();
                }
            }
        },
        async getAIStuff() {
            let links = this.liked.map((x)=>{
                console.log(x);
                return x.image_url
            });
            if (links.length > 10) {
                links = links.slice(0, 10);
            }
            this.aiStuff = await (await fetch(`${this.server}aistuff?links=${encodeURIComponent(JSON.stringify(links))}`, {
                method: "GET",
                headers: {
                    "Ngrok-Skip-Browser-Warning": "69420",
                }
            })).json();
        },
        async right() {
            if (this.queue === null || this.queue.length == 0) {
                if (this.liked.length >= 9 && this.finished != true) {
                    this.finished = true;
                    this.getAIStuff();
                }
                return;
            }
            const current = this.queue.shift();
            this.liked.push(current);
            if (this.liked.length >= 9) {
                this.removeCounter = 0; 
                return;
            };
            const newItems = await (await fetch(`${this.server}right?title=${current.image_title}`, {
                method: "GET",
                headers: {
                    "Ngrok-Skip-Browser-Warning": "69420",
                }
            })).json();
            newItems.forEach(element => {
                if (this.queue == null) this.queue = []
                this.queue.push(element);
            });
            if (this.queue == null || this.queue.length == 0) {
                console.log(this.liked.length, this.finished);
                if (this.liked.length >= 9 && this.finished != true) {
                    this.finished = true;
                    this.getAIStuff();
                } else {
                    this.queue = null;
                    this.init();
                }
            }
            console.log(this.queue.length);
        },
        async init() {
            this.liked = [];
            this.queue = await (await fetch(this.server+"init", {
                method: "GET",
                headers: {
                    "Ngrok-Skip-Browser-Warning": "69420",
                }
            })).json();
        }
    },
}
</script>

<style scoped>
.shadow-thing {
    filter: drop-shadow(-25px 25px 10px rgba(50, 50, 150, 0.4));
}

.image-thing {
    transition: transform 0.5s linear;
    background-repeat: no-repeat;
    background-size: cover;
    transform: scale(1)
}
.image-thing:hover {
    transform: scale(1.05)
}

.red-arrow {
    @apply transition-transform;
    transform: scaleX(-1);
    cursor:pointer;
    filter: hue-rotate(275deg);
}
.red-arrow:hover {
    transform: scaleX(-1.25) scaleY(1.25) translateX(25px);
}
.green-arrow {
    @apply transition-transform;
    cursor:pointer;
}
.green-arrow:hover {
    transform: scaleX(1.25) scaleY(1.25) translateX(25px);
}
</style>
