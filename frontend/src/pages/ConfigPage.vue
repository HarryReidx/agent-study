<template><div><h3>系统配置</h3><pre>{{cfg}}</pre></div></template>
<script setup>
import {ref,onMounted} from 'vue'; import { http } from '../api/http'
const cfg=ref('')
onMounted(async()=>{const {data}=await http.get('/system/config'); cfg.value=JSON.stringify(data,null,2)})
</script>
