import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import App from '../src/App.vue'

describe('App.vue', () => {
  it('renderiza o título correto', () => {
    const wrapper = mount(App)
    expect(wrapper.find('h1').text()).toBe('Gerenciador de Tarefas')
  })
})