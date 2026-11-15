(* nbtext.wl -- shared by the notebook generators: turns a text string that may contain linear-syntax boxes
   (\!\(\*SubscriptBox[\(a\), \(b\)]\), Superscript-, Overscript-) and named characters (\[MinusSign]) into a TextData
   cell body that the front end typesets. *)
nbBox[in_String] := BoxData[ToExpression[StringReplace[in, {"\\(" -> "\"", "\\)" -> "\""}]]];
nbNamed[s_String] := StringReplace[s, "\\[" ~~ n : WordCharacter .. ~~ "]" :> ToExpression["\"\\[" <> n <> "]\""]];
nbText[s_String] := TextData[Replace[
    StringSplit[s, "\\!\\(\\*" ~~ in : Shortest[__] ~~ "]\\)" :> Cell[nbBox[in <> "]"]]], str_String :> nbNamed[str], {1}]];
