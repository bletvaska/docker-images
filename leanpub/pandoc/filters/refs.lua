-- ---------------------------------------------------------------------------
-- Znizi nadpis automaticky vlozenej sekcie literatury na uroven <h2>.
--
-- Pandoc/citeproc vklada nadpis z 'reference-section-title' ako <h1>.
-- Tento filter najde <div id="refs"> (vytvara ho citeproc) a predchadzajuci
-- Header znizi na level 2.
--
-- MUSI bezat az PO citeproc -> v defaults subore je v 'filters'
-- uvedeny za polozkou 'citeproc'.
-- ---------------------------------------------------------------------------

function Pandoc(doc)
  local blocks = doc.blocks
  for i = 2, #blocks do
    local b = blocks[i]
    if b.t == "Div" and b.identifier == "refs" then
      local prev = blocks[i - 1]
      if prev and prev.t == "Header" and prev.level < 2 then
        prev.level = 2
      end
    end
  end
  return doc
end
