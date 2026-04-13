<template><div><h3>提交工单</h3><input v-model="form.title" placeholder="标题"/><br/><textarea v-model="form.description" placeholder="描述"></textarea><br/><input v-model="form.error_log" placeholder="错误日志"/><br/><select v-model="form.priority"><option>P0</option><option>P1</option><option>P2</option><option>P3</option></select><button @click="submit">提交</button><p>{{ msg }}</p></div></template>
<script setup>
import { ref } from 'vue'; import { http } from '../api/http'
const form = ref({title:'',description:'',error_log:'',priority:'P3'}); const msg = ref('')
const submit = async()=>{ const {data}=await http.post('/tickets',form.value); msg.value='已创建#'+data.id }
</script>
