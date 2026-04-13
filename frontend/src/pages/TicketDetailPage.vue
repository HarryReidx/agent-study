<template><div><h3>工单详情</h3><div v-if="t">#{{t.id}} {{t.title}}<p>分类:{{t.category}} 置信度:{{t.confidence}}</p><p>{{t.suggestion}}</p><button @click="analyze">触发分析</button> <router-link :to="`/tickets/${id}/traces`">查看轨迹</router-link></div></div></template>
<script setup>
import {ref,onMounted} from 'vue'; import { useRoute } from 'vue-router'; import { http } from '../api/http'
const route = useRoute(); const id=route.params.id; const t=ref(null)
const load=async()=>{const {data}=await http.get(`/tickets/${id}`); t.value=data}
const analyze=async()=>{await http.post('/tickets/analyze',{ticket_id:Number(id)}); await load()}
onMounted(load)
</script>
