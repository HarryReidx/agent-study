<template><div><h3>Agent轨迹</h3><ul><li v-for="x in traces" :key="x.id">step{{x.step_no}} {{x.tool_name}} success={{x.success}} input={{x.action_input}} obs={{x.observation}}</li></ul></div></template>
<script setup>
import {ref,onMounted} from 'vue'; import { useRoute } from 'vue-router'; import { http } from '../api/http'
const traces=ref([]); const id=useRoute().params.id
onMounted(async()=>{const {data}=await http.get(`/tickets/${id}/traces`); traces.value=data})
</script>
