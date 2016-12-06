Code Review Notes
---
Notes will be in the form of:

```
line number start-line number end: note
```

---
script.js
--

61: trimming can be done by builtin library.

80: What if getCookie returns null?

80: id_token is never used.

82-91: this should use an event parameter, rather then holding the original xmlHttpRequest.

88: A wild TODO has appeared. Perhaps a batter option would be to resend the request? Also we have the capability to show toasts. 

98: isn't this redundent and can be handled by css?

105, 107, 109: Referencing the same elements through a different means then `33-35`. Please use the shortcuts.

106, 108, 110: Theres also a style property for this, just add a `.hide` class.

127: no explanation of `mirrorEnabled`

127: Is it necessary or can you use `$(".switch input").checked`

135-136: Again, use the shortcuts... please.

139: This seems unnecessary or overkill.

169: Same note about shortcuts.

186: Generalize this to allow any error message perhaps.

188: `x` is not a good variable name.

188: shortcuts!!!

194: Elsewhere this is done by `x.classList.remove("show")` 

194: This should be expanded for readability. 

194: Magic number `3000` should be `3 * SECOND` with a constant variable `SECOND`

212-239: Unnecessary. Can be done by css. (Also again, very overkill).

241: Bad comment considering its not temporary anymore

242: This should be `HOUR`

349: Why are we making a new recorder here? Simply stopping the only one should be sufficent. 

353: this should happen regardless of recorder's existance. 

407: has been done traditionally with `addEventListener`

408: `dataAvailable` may be called for any number of reasons. For clarity sake this should be put in `onStop`.

422: this doesn't accurately reflect the actual choice or the size of the box.

443: this could be done by simply adding the offset if enabled. Also `Math.round()` it.

463-464: this doesn't make sense, and should be `+ buttonScale - smallButtonScale`, and `+buttonScale + smallButtonScale` 

468,470: Same note as above. Better variables should be used....

494: shortcuts.

500-507: the page should be reloaded regardless to utilize the client's cookie in rendering.