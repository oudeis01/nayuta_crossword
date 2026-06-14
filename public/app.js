// 격자 칸 탭 -> 단어 선택/토글 -> 하단 시트(비모달)로 해당 단어 힌트 표시.
// 비모달이라 시트가 떠 있어도 격자는 계속 탭된다(다른 단어 전환/방향 토글 가능).
// 정적 사이트라 의존성 없음. 데이터는 페이지 인라인 JSON(#slot-data).
(function () {
  var data = {};
  try { data = JSON.parse(document.getElementById('slot-data').textContent || '{}'); }
  catch (e) { data = {}; }

  var grid = document.querySelector('.grid');
  var sheet = document.getElementById('sheet');
  var titleEl = document.getElementById('sheet-title');
  var bodyEl = document.getElementById('sheet-body');
  var closeBtn = document.getElementById('sheet-close');
  if (!grid || !sheet) return;

  var current = null;     // 현재 선택 슬롯 id (문자열)

  function clearSel() {
    var on = grid.querySelectorAll('.cell.sel');
    for (var i = 0; i < on.length; i++) on[i].classList.remove('sel');
  }

  function highlight(id) {
    clearSel();
    var cells = grid.querySelectorAll('[data-a="' + id + '"],[data-d="' + id + '"]');
    for (var i = 0; i < cells.length; i++) cells[i].classList.add('sel');
  }

  function render(id) {
    var slot = data[id];
    if (!slot) return;
    titleEl.textContent = slot.dir + ' ' + slot.num + ' · ' + slot.len + ' letters';
    bodyEl.innerHTML = '';
    if (slot.given) {
      var g = document.createElement('p');
      g.className = 'note';
      g.textContent = 'This word is already filled in on the grid.';
      bodyEl.appendChild(g);
      return;
    }
    if (!slot.hints || !slot.hints.length) {
      var nn = document.createElement('p');
      nn.className = 'note';
      nn.textContent = 'No example available for this word yet.';
      bodyEl.appendChild(nn);
      return;
    }
    for (var i = 0; i < slot.hints.length; i++) {
      var h = slot.hints[i];
      var ex = document.createElement('div');
      ex.className = 'ex';
      var p = document.createElement('p');
      p.className = 'sent';
      p.innerHTML = h.html;
      ex.appendChild(p);
      if (h.url) {
        var a = document.createElement('a');
        a.className = 'src';
        a.href = h.url;
        a.target = '_blank';
        a.rel = 'noopener';
        a.textContent = h.domain || 'source';
        ex.appendChild(a);
      }
      bodyEl.appendChild(ex);
    }
  }

  function openSheet(id) {
    current = id;
    highlight(id);
    render(id);
    sheet.hidden = false;
    sheet.classList.remove('closing');
    // 선택 칸이 시트에 가리지 않도록 위쪽으로 부드럽게 스크롤.
    var first = grid.querySelector('.cell.sel');
    if (first && first.scrollIntoView) first.scrollIntoView({block: 'center', behavior: 'smooth'});
  }

  function closeSheet() {
    if (sheet.hidden) return;
    sheet.classList.add('closing');
    clearSel();
    current = null;
    var done = function () {
      sheet.hidden = true;
      sheet.classList.remove('closing');
      sheet.removeEventListener('transitionend', done);
    };
    sheet.addEventListener('transitionend', done);
    setTimeout(done, 300);  // transition 미발생 환경 대비 폴백
  }

  // 비모달이라 문서 전역에서 탭을 받는다:
  //  - 클루 칸 탭 -> 선택/전환(교차칸 재탭은 방향 토글)
  //  - 시트 내부 탭 -> 무시
  //  - 그 외(검은칸/여백) 탭 -> 시트 닫기
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (sheet.contains(t)) return;
    var cell = t.closest ? t.closest('.cell.clue') : null;
    if (!cell) { closeSheet(); return; }
    var a = cell.getAttribute('data-a');
    var d = cell.getAttribute('data-d');
    var opts = [];
    if (a) opts.push(a);
    if (d) opts.push(d);
    if (!opts.length) { closeSheet(); return; }
    var pick;
    if (opts.length === 1) {
      pick = opts[0];
    } else if (current && opts.indexOf(current) !== -1) {
      pick = opts[(opts.indexOf(current) + 1) % 2];  // 같은 교차칸 재탭 -> 방향 전환
    } else {
      pick = opts[0];
    }
    openSheet(pick);
  });

  closeBtn.addEventListener('click', closeSheet);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !sheet.hidden) closeSheet();
  });

  // 핸들 스와이프다운으로 닫기 (모바일).
  var startY = null;
  sheet.addEventListener('touchstart', function (e) {
    if (e.touches && e.touches.length === 1) startY = e.touches[0].clientY;
  }, { passive: true });
  sheet.addEventListener('touchmove', function (e) {
    if (startY === null) return;
    var dy = e.touches[0].clientY - startY;
    if (dy > 60 && sheet.scrollTop <= 0) { closeSheet(); startY = null; }
  }, { passive: true });
  sheet.addEventListener('touchend', function () { startY = null; });
})();
