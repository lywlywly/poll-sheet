<template>
    <p>We advise against editing directly in the browser since you could lose your work due to server shutdown. However, it is recommended to paste your note below and check if the markdown is rendered correctly.</p>
    <div class="grid-container">
        <textarea v-model="markdown"></textarea>
        <div v-html="markdownToHtml"></div>
    </div>
    <button @click="print">Submit</button>
</template>
<script>
import { marked } from 'marked';

export default {
    name: 'App',
    data() {
        return {
            markdown: "# Note Example\n### Java variables\n* Primitive types\n  * int\n  * double\n* Objects\n  * Integer\n  * Double",
        };
    },
    computed: {
        markdownToHtml() {
            return marked(this.markdown);
        }
    },
    methods: {
        print() {
            alert(("Not Implemented"))
            console.log(localStorage.token)
        },
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

.grid-container {
    display: grid;
    grid-template-columns: auto auto;
    grid-template-rows: auto;
    gap: 10px;
    background-color: #2196F3;
    padding: 10px;
}

.grid-container>div {
    background-color: rgba(255, 255, 255, 0.8);
    text-align: left;
    padding: 20px 0;
    /* font-size: 30px; */
}
</style>