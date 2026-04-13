<template>
  <div>
    <h2>工单智能分诊学习平台</h2>
    <nav>
      <router-link to="/submit">提交</router-link> |
      <router-link to="/tickets">列表</router-link> |
      <router-link to="/eval">Eval</router-link> |
      <router-link to="/config">配置</router-link>
    </nav>
    <router-view />
  </div>
</template>
