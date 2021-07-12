/* jshint esversion: 6 */

$(document).ready(function () {
    // number all steps
    let step = 1;
    $('h3.step').each(function () {
        $(this).prepend(`Krok #${step}: `);

        // mark all tasks
        let task = 1;
        $(this).nextUntil('.step', '.task + p').each(function(){
            $(this).addClass('alert alert-success');
            $(this).prepend(`<b>Úloha ${step}.${task}:</b> `);
            task++;
        });

        step++;
    });

    // hide all the task
    $('.task').hide();
});
