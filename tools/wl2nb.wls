(* wl2nb.wls -- turn a structured Mathematica script into a notebook with outputs.
   Usage (from Notes/):  tools/wl.sh tools/wl2nb.wls code/mma/<script>.wls [out.nb]
   Script structure (house rule, 2026-10-13): optional setup code, then blocks
       (*@ N. Title | One to three sentences: what this step does and why, and which equation it produces. @*)
       code for this one step; its last expression is what the step produces (printed: an equation, not True)
   An optional first header (*@@ Notebook title | Introduction @@*) gives the title and an intro paragraph.
   Each block becomes: a subsection (title), a text cell, a code cell, the prints of the code, and its value.
   Generator variables carry the prefix wl2nb so they cannot collide with the script's symbols. *)
With[{d = DirectoryName[$InputFileName]}, Get[First[Select[{FileNameJoin[{d, "nbtext.wl"}], FileNameJoin[{d, "..", "code", "mma", "nbtext.wl"}]}, FileExistsQ]]]];
wl2nbIn = $ScriptCommandLine[[2]];
wl2nbOut = If[Length[$ScriptCommandLine] >= 3, $ScriptCommandLine[[3]], StringReplace[wl2nbIn, ".wls" ~~ EndOfString -> ".nb"]];
wl2nbSrc = Import[wl2nbIn, "Text"];
(* optional notebook header *)
wl2nbHead = StringCases[wl2nbSrc, "(*@@" ~~ h : Shortest[__] ~~ "@@*)" :> h, 1];
{wl2nbTitle, wl2nbIntro} = If[wl2nbHead === {}, {FileBaseName[wl2nbIn], ""},
   StringTrim /@ Append[StringSplit[First[wl2nbHead], "|", 2], ""][[;; 2]]];
wl2nbSrc = StringReplace[wl2nbSrc, "(*@@" ~~ Shortest[__] ~~ "@@*)" -> "", 1];
wl2nbParts = StringSplit[wl2nbSrc, "(*@"];
wl2nbSetup = StringTrim[StringReplace[First[wl2nbParts], StartOfString ~~ "#!" ~~ Shortest[___] ~~ "\n" -> ""]];
wl2nbBlocks = Rest[wl2nbParts];
wl2nbCells = Join[{Cell[wl2nbTitle, "Title"]}, If[wl2nbIntro === "", {}, {Cell[nbText[wl2nbIntro], "Text"]}]];
wl2nbRun[wl2nbCode_String] := Module[{wl2nbVal, wl2nbPr},
   {wl2nbVal, wl2nbPr} = Reap[Block[{Print = Sow[Row[{##}]] &}, ToExpression[wl2nbCode]]];
   Join[{Cell[wl2nbCode, "Code", PageWidth -> WindowWidth]},
    If[wl2nbPr === {}, {}, Cell[BoxData[ToBoxes[#, StandardForm]], "Print"] & /@ First[wl2nbPr]],
    If[wl2nbVal === Null, {}, {Cell[BoxData[ToBoxes[wl2nbVal, StandardForm]], "Output"]}]]];
If[StringTrim[StringReplace[wl2nbSetup, "(*" ~~ Shortest[___] ~~ "*)" -> ""]] =!= "", wl2nbCells = Join[wl2nbCells, {Cell["Setup", "Subsection"]}, wl2nbRun[wl2nbSetup]]];
Do[
  Module[{wl2nbHd, wl2nbCd, wl2nbT, wl2nbX},
   {wl2nbHd, wl2nbCd} = StringSplit[wl2nbB, "@*)", 2];
   {wl2nbT, wl2nbX} = StringTrim /@ Append[StringSplit[wl2nbHd, "|", 2], ""][[;; 2]];
   wl2nbCells = Join[wl2nbCells, {Cell[wl2nbT, "Subsection"]}, If[wl2nbX === "", {}, {Cell[nbText[wl2nbX], "Text"]}],
     wl2nbRun[StringTrim[wl2nbCd]]];
   Print[wl2nbT]],
  {wl2nbB, wl2nbBlocks}];
Export[wl2nbOut, Notebook[wl2nbCells]];
Print["written ", wl2nbOut, ", ", Length[wl2nbCells], " cells"];
