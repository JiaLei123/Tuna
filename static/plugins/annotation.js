/**
 * Created by JiaLei on 2017/7/9.
 */
function  a () {
    $(function () {
        var a, b, c, d, e;
        c = "#annotation-work-area", b = "#annotation-box", e = "selection-frame";
        if ($(c).is("*"))return ko.bindingHandlers.annotationComponentDrop = {
            init: function (a, b, c, d) {
                var e, f;
                return f = b(), e = f.annotation, $(a).drop(function (a, b) {
                    return e.dragToSelect("drop", d)
                })
            }
        }, window.annotation = new Annotation, ko.applyBindings(annotation, $(c)[0]), a = $(b), a.drag("start", function (b, c) {
            return b.stopPropagation(), annotation.dragToSelect("start", {ctrlKey: b.ctrlKey}), $("<div />").addClass(e).appendTo(a)
        }).drag(function (b, c) {
            var d, e, f, g, h, i, j, k, l, m, n;
            return e = a.position(), f = a.innerWidth(), d = a.innerHeight(), g = {
                left: b.pageX - e.left,
                top: b.pageY - e.top
            }, l = {
                left: c.startX - e.left,
                top: c.startY - e.top
            }, i = Math.min(g.top, l.top), h = Math.min(g.left, l.left), m = Math.max(i, 0), k = Math.max(h, 0), j = Math.min(Math.abs(g.top - l.top) - Math.abs(m - i), d - m), n = Math.min(Math.abs(g.left - l.left) - Math.abs(k - h), f - k), $(c.proxy).css({
                top: m,
                left: k,
                height: j,
                width: n
            })
        }).drag("end", function (a, b) {
            return $(b.proxy).remove(), annotation.dragToSelect("end")
        }), $.drop({multi: !0}), d = function () {
            return BootstrapAlerts.error(I18n.annotations.annotation_work_area.errors.load_data_error, !1)
        }, $.ajax("", {
            dataType: "json", success: function (a) {
                var b, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, A, B, C, D, E, F, G;
                annotation.populate(a), b = $("#parse-type-group-input"), d = $("#parse-type-input"), u = a.parse_type_groups.slice(0), h = function (a) {
                    return u.filter(function (b) {
                        return a.indexOf(parseInt(b.id)) >= 0
                    })
                }, i = function (a, b) {
                    return j(a, b) ? b.content[0] : F(a, b)
                }, F = function (a, b) {
                    var c;
                    c = b.content.filter(function (b) {
                        return b.label === a
                    });
                    if (c.length === 1)return c[0]
                }, j = function (a, b) {
                    return b.content.length === 1 && a === b.content[0].label
                }, x = {}, k = function (a) {
                    return x[a] = !0
                }, G = function (a) {
                    return delete x[a]
                }, y = function (a) {
                    return !!x[a]
                }, D = function (a) {
                    return d.parseTypeAutocomplete("option", "source", a.slice(0))
                }, w = function (a) {
                    var b;
                    if (y("parseTypeGroup"))return;
                    return b = function (a) {
                        var b;
                        return b = a.map(function (a) {
                            return parseInt(a.value)
                        }), h(b)
                    }, D(b(a)), k("parseType")
                }, C = function (a) {
                    return b.parseTypeGroupAutocomplete("option", "source", a.slice(0))
                }, v = function (a) {
                    var b;
                    if (y("parseType"))return;
                    return b = function (a) {
                        var b;
                        return b = a.reduce(function (a, b) {
                            var c;
                            return c = parseInt($.custom.parseTypeAutocomplete.extractIds(b.value)[0]), a.indexOf(c) >= 0 || a.push(c), a
                        }, []), h(b)
                    }, C(b(a)), k("parseTypeGroup")
                }, r = function (a) {
                    var b;
                    return b = {}, u.some(function (c) {
                        if (c.id === a)return b = c
                    }), b
                }, o = function (a, b) {
                    var c;
                    return c = {}, a.some(function (a) {
                        if (a.id === b)return c = a
                    }), c
                }, A = function (a) {
                    var b, c, d, e;
                    return b = a != null ? a.value : void 0, c = [null, null], (b != null ? b.length : void 0) > 0 && (c = $.custom.parseTypeAutocomplete.extractIds(b), e = r(c[0]), d = o(e.parse_types, c[1])), annotation.parseTypeGroup().setAttributes(e || {}, d || {})
                }, B = function (a) {
                    var b, c;
                    return c = a && parseInt(a.value) || null, b = c && r(c) || {}, annotation.parseTypeGroup().setAttributes(b)
                }, f = function (a) {
                    return b.val(a.group.name), d.val(a.label)
                }, E = function () {
                    var a;
                    if (a = d.val())return d.parseTypeAutocomplete("search", a)
                }, g = function () {
                    var a;
                    a = d.parseTypeAutocomplete("option", "source");
                    if (a.length === 1)return d.val(a[0].label)
                }, b.parseTypeGroupAutocomplete({
                    delay: 0,
                    minLength: 0,
                    appendTo: c + " .parse-type-group-input-container",
                    source: u.slice(0),
                    focus: function () {
                        return !1
                    },
                    open: function () {
                        var a;
                        return a = $(this).parseTypeGroupAutocomplete("widget")[0], makeElementNotExceedWindowVertically(a)
                    },
                    select: function (a, c) {
                        return b.val(c.item.label), B(c.item), w([c.item]), g(), E(), !1
                    },
                    response: function (a, c) {
                        var d, e;
                        e = b.val();
                        if (d = i(e, c)) $(this).parseTypeGroupAutocomplete("close"), g(), E();
                        return B(d), e && e.length > 0 ? w(c.content) : (D(u), G("parseType"))
                    }
                }).on("focus", function () {
                    return $(this).parseTypeGroupAutocomplete("search", $(this).val())
                }), d.parseTypeAutocomplete({
                    delay: 0,
                    minLength: 0,
                    appendTo: c + " .parse-type-input-container",
                    source: u.slice(0),
                    focus: function () {
                        return !1
                    },
                    open: function () {
                        var a;
                        return a = $(this).parseTypeAutocomplete("widget")[0], makeElementNotExceedWindowVertically(a)
                    },
                    select: function (a, b) {
                        return annotation.untagSentence(), f(b.item), A(b.item), v([b.item]), !1
                    },
                    response: function (a, b) {
                        var c, e, g, h;
                        h = d.val();
                        if (g = i(h, b)) $(this).parseTypeAutocomplete("close"), f(g), c = annotation.parseTypeGroup().id(), e = annotation.parseTypeGroup().parseType().id(), $.custom.parseTypeAutocomplete.composeId(c, e) !== g.value && annotation.untagSentence();
                        return A(g), h && h.length > 0 ? v(b.content) : (C(u), G("parseTypeGroup"))
                    }
                }).on("focus", function () {
                    return $(this).parseTypeAutocomplete("search", $(this).val())
                }), z = function () {
                    return makeElementNotExceedWindowVertically(d.parseTypeAutocomplete("widget")[0]), makeElementNotExceedWindowVertically(b.parseTypeGroupAutocomplete("widget")[0])
                }, $(window).scroll(z).resize(z);
                if (annotation.completed())return s = a.parse_type_group_id, t = a.parse_type_id, q = r(s), n = o(q.parse_types, t), annotation.parseTypeGroup().setAttributes(q, n), b.val(annotation.parseTypeGroup().name()), d.val(annotation.parseTypeGroup().parseType().name());
                if (!(e = a.cluster) || e === "")return b.focus();
                e = e.toLowerCase(), m = a.parse_type_groups.filter(function (a) {
                    return a.name.toLowerCase() === e
                });
                switch (m.length) {
                    case 1:
                        return l = m[0], p = l.name, b.val(p).change(), b.parseTypeGroupAutocomplete("search", p), d.focus();
                    default:
                        return b.focus()
                }
            }, error: d
        }), $("#parse-type-group-input").on("blur", function () {
            return $(this).parseTypeGroupAutocomplete("close")
        }), $("#parse-type-input").on("blur", function () {
            return $(this).parseTypeAutocomplete("close")
        }), $(c).on("keyup", "#search-tag", function () {
            return annotation.tagFilteringTerm($(this).val())
        }), $(c).on("change", "#search-tag", function () {
            return annotation.tagFilteringTerm($(this).val())
        })
    })
}

a.call(this)