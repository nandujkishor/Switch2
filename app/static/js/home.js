function show(){
  $('body').removeClass('noscroll');
  $('.down-arrow, .coming-soon, .dates').addClass('show');

}

function b1(){
  
  class TextScramble {
    constructor(el) {
      this.el = el
      this.chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      this.update = this.update.bind(this)
    }
    setText(newText) {
      const oldText = this.el.innerText
      const length = Math.max(oldText.length, newText.length)
      const promise = new Promise((resolve) => this.resolve = resolve)
      this.queue = []
      for (let i = 0; i < length; i++) {
        const from = oldText[i] || ''
        const to = newText[i] || ''
        const start = Math.floor(Math.random() * 40)
        const end = start + Math.floor(Math.random() * 40)
        this.queue.push({ from, to, start, end })
      }
      cancelAnimationFrame(this.frameRequest)
      this.frame = 0
      this.update()
      return promise
    }
    update() {
      let output = ''
      let complete = 0
      for (let i = 0, n = this.queue.length; i < n; i++) {
        let { from, to, start, end, char } = this.queue[i]
        if (this.frame >= end) {
          complete++
          output += to
        } else if (this.frame >= start) {
          if (!char || Math.random() < 0.28) {
            char = this.randomChar()
            this.queue[i].char = char
          }
          output += `<span class="text">${char}</span>`
        } else {
          output += from
        }
      }
      this.el.innerHTML = output
      if (complete === this.queue.length) {
        this.resolve()
      } else {
        this.frameRequest = requestAnimationFrame(this.update)
        this.frame++
      }
    }
    randomChar() {
      return this.chars[Math.floor(Math.random() * this.chars.length)]
    }
  }
  
  phrases = [
    'TECHNOLOGY',
    'EXPLORATION',
    'ENTERTAINMENT',
    'VIDYUT'
  ]

  // console.log($.cookie("home"));

  const el = document.querySelector('.counter')
  const fx = new TextScramble(el)
  let counter = 0, n = 0, check = 3

  if($.cookie("home")){
    phrases = [
      'VIDYUT'
    ]
    check = 0
  }

  const next = () => {
    n++;
    fx.setText(phrases[counter]).then(() => {
      
      if(n == 4 || $.cookie("home")){
        window.setTimeout(function(){
          show();
          $.cookie("home", true);
        },1000)
      }

      if(n <= check)
        setTimeout(next, 1000)
    
    })
    counter = (counter + 1) % phrases.length
  }
  next()

}