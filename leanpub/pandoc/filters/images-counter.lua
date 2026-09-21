--[[
Prepend "Obr. N: " to every figure's caption when writing HTML, numbering
figures in document order, and tag every image with the "img-responsive"
class.

Pandoc promotes a standalone image paragraph to its own "Figure" block with
a separate caption, so the visible caption and the image's own alt text
have to be updated independently (a plain Image filter alone only reaches
the alt text).
]]

local counter = 0

function Image(elem)
  if FORMAT ~= 'html' then return nil end

  elem.classes:insert('img-responsive')
  return elem
end

function Figure(elem)
  if FORMAT ~= 'html' then return nil end

  counter = counter + 1
  local prefix = 'Obr. ' .. counter .. ': '

  -- visible <figcaption>
  local caption = elem.caption.long
  if caption and #caption > 0 then
    table.insert(caption[1].content, 1, pandoc.Strong({ pandoc.Str(prefix) }))
  end

  -- <img alt="...">
  elem.content = elem.content:walk({
    Image = function(img)
      table.insert(img.caption, 1, pandoc.Strong({ pandoc.Str(prefix) }))
      return img
    end
  })

  return elem
end
