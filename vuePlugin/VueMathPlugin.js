export default{
    install:function(Vue){
         // 自定义指令square ，v-square
        Vue.directive('square',function(el,binding){
            el.innerHTML = Math.pow(binding.value,2)
    });
        Vue.directive('sqrt',function(el,binding){
            el.innerHTML = Math.sqrt(binding.value)
    });
        Vue.directive('sin',function(el,binding){
            el.innerHTML = Math.sin(binding.value*Math.PI/180)
    });
        Vue.directive('cos',function(el,binding){
            el.innerHTML = Math.cos(binding.value*Math.PI/180)
    });
        Vue.directive('tan',function(el,binding){
            el.innerHTML = Math.tan(binding.value*Math.PI/180)
    })
    }
}