import { createRouter, createWebHistory } from 'vue-router'
import SubmitPage from '../pages/SubmitPage.vue'
import TicketListPage from '../pages/TicketListPage.vue'
import TicketDetailPage from '../pages/TicketDetailPage.vue'
import TracePage from '../pages/TracePage.vue'
import EvalPage from '../pages/EvalPage.vue'
import ConfigPage from '../pages/ConfigPage.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/tickets' },
    { path: '/submit', component: SubmitPage },
    { path: '/tickets', component: TicketListPage },
    { path: '/tickets/:id', component: TicketDetailPage, props: true },
    { path: '/tickets/:id/traces', component: TracePage, props: true },
    { path: '/eval', component: EvalPage },
    { path: '/config', component: ConfigPage }
  ]
})
