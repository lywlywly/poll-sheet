<script setup></script>

<template>
  <header>
    <!-- <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" /> -->
    <!-- <h1>Header Placeholder</h1> -->
  </header>
  <nav>
    <a href="/form/1" class="nav-link">BK1-Proposal</a>
    <a href="/form/2" class="nav-link">BK1-Presentation</a>
    <!-- <router-link to="/note">Note</router-link> -->
    <!-- <router-link to="/visualization">Visualization</router-link> -->
    <router-link to="/about">About</router-link>
  </nav>

  <br />
  <RouterView class="main-app-view" name="about" />
  <RouterView />
</template>

<style scoped>
/* a {
  display: inline-block;
  background-color: black;
  border: solid 1px black;
  color: white;
  padding: 5px;
  margin: 10px;
}

a:hover,
a.router-link-active {
  background-color: rgb(110, 79, 13);
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
} */

nav {
  width: 100%;
  font-size: 15px;
  text-align: center;
  margin-top: 2rem;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid;
}

nav a:first-of-type {
  border: 0;
}
</style>
