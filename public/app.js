// 상하 분할: 격자 칸 탭 -> 단어 선택/토글 -> 화면 하단 고정 패널에 그 단어 힌트 표시.
// 패널은 격자와 겹치지 않는 별개 영역이라 격자는 항상 보이고 계속 탭된다(재탭 토글 정상).
// 교차칸은 패널 헤더의 Across/Down 토글 버튼으로도 방향 전환 가능.
// 정적 사이트라 의존성 없음. 데이터는 페이지 인라인 JSON(#slot-data).
(function () {
  var data = {};
  try { data = JSON.parse(document.getElementById('slot-data').textContent || '{}'); }
  catch (e) { data = {}; }

  var grid = document.querySelector('.grid');
  var panel = document.getElementById('hints');
  var titleEl = document.getElementById('hints-title');
  var toggleEl = document.getElementById('hints-toggle');
  var bodyEl = document.getElementById('hints-body');
  var closeBtn = document.getElementById('hints-close');
  if (!grid || !panel) return;

  var current = null;   // 현재 선택 슬롯 id (문자열)
  var curOpts = [];     // 마지막 탭한 칸의 [가로, 세로] 슬롯 id (방향 토글 대상)

  function clearSel() {
    var on = grid.querySelectorAll('.cell.sel');
    for (var i = 0; i < on.length; i++) on[i].classList.remove('sel');
  }

  function highlight(id) {
    clearSel();
    var cells = grid.querySelectorAll('[data-a="' + id + '"],[data-d="' + id + '"]');
    for (var i = 0; i < cells.length; i++) cells[i].classList.add('sel');
  }

  function renderToggle() {
    toggleEl.innerHTML = '';
    if (curOpts.length < 2) { toggleEl.hidden = true; return; }
    toggleEl.hidden = false;
    for (var i = 0; i < curOpts.length; i++) {
      (function (id) {
        var slot = data[id];
        var b = document.createElement('button');
        b.type = 'button';
        b.textContent = slot ? (slot.dir + ' ' + slot.num) : id;
        if (id === current) b.className = 'on';
        b.addEventListener('click', function () { if (id !== current) select(id); });
        toggleEl.appendChild(b);
      })(curOpts[i]);
    }
  }

  function renderBody(slot) {
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

  function select(id) {
    var slot = data[id];
    if (!slot) return;
    current = id;
    highlight(id);
    titleEl.textContent = slot.dir + ' ' + slot.num + ' · ' + slot.len + ' letters';
    renderToggle();
    renderBody(slot);
    panel.hidden = false;
    requestAnimationFrame(function () { panel.classList.add('in'); });
    // 선택 칸이 패널 위쪽 격자 영역 안에 보이도록 스크롤(패널과 겹치지 않음).
    var first = grid.querySelector('.cell.sel');
    if (first && first.scrollIntoView) first.scrollIntoView({block: 'center', behavior: 'smooth'});
  }

  function closePanel() {
    if (panel.hidden) return;
    panel.classList.remove('in');
    clearSel();
    current = null;
    curOpts = [];
    panel.hidden = true;
  }

  // 문서 전역 탭 처리:
  //  - 클루 칸 탭 -> 선택/전환(교차칸 재탭은 방향 토글)
  //  - 패널 내부 탭 -> 패널이 처리(닫기/토글 버튼)
  //  - 그 외(검은칸/여백) 탭 -> 패널 닫기
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (panel.contains(t)) return;
    var cell = t.closest ? t.closest('.cell.clue') : null;
    if (!cell) { closePanel(); return; }
    var a = cell.getAttribute('data-a');
    var d = cell.getAttribute('data-d');
    var opts = [];
    if (a) opts.push(a);
    if (d) opts.push(d);
    if (!opts.length) { closePanel(); return; }
    curOpts = opts;
    var pick;
    if (opts.length === 1) {
      pick = opts[0];
    } else if (current && opts.indexOf(current) !== -1) {
      pick = opts[(opts.indexOf(current) + 1) % 2];  // 같은 교차칸 재탭 -> 방향 전환
    } else {
      pick = opts[0];
    }
    select(pick);
  });

  closeBtn.addEventListener('click', closePanel);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) closePanel();
  });
})();
