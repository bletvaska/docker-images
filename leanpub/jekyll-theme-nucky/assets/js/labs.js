/* jshint esversion: 6 */

document.addEventListener('DOMContentLoaded', function () {
    // number all steps
    let step = 1;

    document.querySelectorAll('h3.step').forEach(function (stepEl) {
        stepEl.insertAdjacentHTML('afterbegin', `Krok #${step}: `);

        // mark all tasks
        let task = 1;
        let sibling = stepEl.nextElementSibling;
        while (sibling && !sibling.classList.contains('step')) {
            if (sibling.matches('.task + p')) {
                sibling.classList.add('alert', 'alert-success');
                sibling.insertAdjacentHTML('afterbegin', `<b>Úloha ${step}.${task}:</b> `);
                task++;
            }
            sibling = sibling.nextElementSibling;
        }

        step++;
    });

    // hide all the task
    document.querySelectorAll('.task').forEach(function (el) {
        el.style.display = 'none';
    });
});
