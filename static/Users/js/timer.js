var Clock = (function(){
    var exports = function(element) {
      this._element = element;
      var html = '';
      for (var i=0;i<6;i++) {
        html += '<span>&nbsp;</span>';
      }
      this._element.innerHTML = html;
      this._slots = this._element.getElementsByTagName('span');
      this._tick();
    };
    exports.prototype = {
      _tick:function() {
        var time = new Date().getTime();
        var end=new Date("Feb 09, 2021 02:00:25").getTime();
        var distance= end-time;

        if(distance == 0){
          window.location.replace('{% url 'logout' %}');
             if(window.location.port != "")
                 window.location=window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/logout/';
             else
                 window.location=window.location.protocol + '//' + window.location.hostname + '/logout/';
        }

        // Time calculations for days, hours, minutes and seconds
          //var days = Math.floor(distance / (1000 * 60 * 60 * 24));
          var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
          var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
          var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        this._update(this._pad(hours) + this._pad(minutes) + this._pad(seconds));
        var self = this;
        setTimeout(function(){
          self._tick();
        },1000);
      },
      _pad:function(value) {
        return ('0' + value).slice(-2);
      },
      _update:function(timeString) {
        var i=0,l=this._slots.length,value,slot,now;
        for (;i<l;i++) {
          value = timeString.charAt(i);
          slot = this._slots[i];
          now = slot.dataset.now;
          if (!now) {
            slot.dataset.now = value;
            slot.dataset.old = value;
            continue;
          }
          if (now !== value) {
            this._flip(slot,value);
          }
        }
      },
      _flip:function(slot,value) {
        slot.classList.remove('flip');
        slot.dataset.old = slot.dataset.now;
        slot.dataset.now = value;
        slot.offsetLeft;
        slot.classList.add('flip');
      }
    };
    return exports;
  }());
  var i=0,clocks = document.querySelectorAll('.clock'),l=clocks.length;
  for (;i<l;i++) {
    new Clock(clocks[i]);
  }