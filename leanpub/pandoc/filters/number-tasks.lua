--[[
Number headers marked with the "task" class as "<step>.<task>", where
<step> increments on each header marked with the "step" class.
]]

local step = 0
local task = 0

-- FIXME treba vyriesit cislovanie pre epub - header 1 nuluje step
function Header(elem)
  if FORMAT == 'html' or FORMAT == 'epub' then
    if elem.classes:includes('step') then
      step = step + 1
      task = 1
    elseif elem.classes:includes('task') then
      elem.content:insert(pandoc.Space())
      elem.content:insert(pandoc.Str(step .. '.' .. task))
      task = task + 1
    end

    return elem
  end
end
