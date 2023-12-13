<template>
    <!-- {{ markdown }} -->
    <!-- <textarea v-model="markdown"></textarea> -->
    <div v-html="markdownToHtml"></div>

</template>
<script>
import { marked } from 'marked';
import md from '../assets/HelloWorld.md?raw';

export default {

    name: 'App',
    data() {
        return {
            markdown: "# Hello World",
        };
    },
    computed: {
        markdownToHtml() {
            return marked(md);
        }
    }
}
</script>
<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    /* text-align: center; */
    color: #2c3e50;
    /* margin-top: 60px; */
}
</style>