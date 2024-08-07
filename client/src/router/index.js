import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/layout'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/guichen',
    children: [{
      path: 'guichen',
      component: (resolve) => require(['@/views/guichen/index'], resolve),
    },
    {
      path: '/anli',
      component: (resolve) => require(['@/views/anli/index'], resolve),
    }]
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
