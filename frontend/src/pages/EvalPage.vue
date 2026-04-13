<template><div><h3>Eval评测</h3><button @click="run">执行默认评测</button><pre>{{result}}</pre></div></template>
<script setup>
import {ref} from 'vue'; import { http } from '../api/http'
const result=ref('')
const run=async()=>{const {data}=await http.post('/evals/run',{dataset_name:'default'}); result.value=JSON.stringify(data,null,2)}
</script>
