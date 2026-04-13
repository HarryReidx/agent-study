<template><div><h3>工单列表</h3><button @click="load">刷新</button><ul><li v-for="t in list" :key="t.id">#{{t.id}} {{t.title}} [{{t.status}}] <router-link :to="`/tickets/${t.id}`">详情</router-link></li></ul></div></template>
<script setup>
import { ref,onMounted } from 'vue'; import { http } from '../api/http'
const list = ref([]); const load=async()=>{const {data}=await http.get('/tickets'); list.value=data}; onMounted(load)
</script>
