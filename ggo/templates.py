# -*- coding: utf-8 -*-
"""
File: templates.py
Author: Einar Uvsløkk <einar.uvslokk@linux.com>
License: GNU General Public License (GPL) version 3 or later
Description: GObject boilerplates for C source/header files
"""

HEADER = """\
/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 2; tab-width: 2 -*- */
/*
 * {filename}.h
 * This file is part of {cc_prefix}.
 *
 * Copyright (c) 2011 {author} <{email}>
 *
{license}\
 */

#ifndef _{uc}_H_
#define _{uc}_H_

#include <glib-object.h>

G_BEGIN_DECLS

#define {uc_prefix}_TYPE_{uc_suffix}          \
({lc}_get_type ())
#define {uc}(o)            \
(G_TYPE_CHECK_INSTANCE_CAST ((o), {uc_prefix}_TYPE_{uc_suffix}, {cc}))
#define {uc}_CLASS(k)      \
(G_TYPE_CHECK_CLASS_CAST ((k), {uc_prefix}_TYPE_{uc_suffix}, {cc}Class))
#define {uc_prefix}_IS_{uc_suffix}(o)         \
(G_TYPE_CHECK_INSTANCE_TYPE ((o), {uc_prefix}_TYPE_{uc_suffix}))
#define {uc_prefix}_IS_{uc_suffix}_CLASS(k)   \
(G_TYPE_CHECK_CLASS_TYPE ((k), {uc_prefix}_TYPE_{uc_suffix}))
#define {uc}_GET_CLASS(o)  \
(G_TYPE_INSTANCE_GET_CLASS ((o), {uc_prefix}_TYPE_{uc_suffix}, {cc}Class))

typedef struct _{cc}        {cc};
typedef struct _{cc}Class   {cc}Class;
typedef struct _{cc}Private {cc}Private;

struct _{cc}
{{
\tGObject parent;
\t/*< private >*/
\t{cc}Private *priv;
}};

struct _{cc}Class
{{
\tGObjectClass parent_class;
}};

GType {lc}_get_type (void) G_GNUC_CONST;
{cc} * {lc}_new (void);

G_END_DECLS

#endif /* _{uc}_H__ */
"""

SOURCE = """\
/* -*- Mode: C; indent-tabs-mode: t; c-basic-offset: 2; tab-width: 2 -*- */
/*
 * {filename}.c
 * This file is part of {cc_prefix}.
 *
 * Copyright (c) 2011 {author} <{email}>
 *
{license}\
 */

#include <config.h>

#include "{filename}.h"

#define {uc}_GET_PRIVATE(o) \\
\t\t(G_TYPE_INSTANCE_GET_PRIVATE ((o),\\
\t\t\t{uc_prefix}_TYPE_{uc_suffix}, {cc}Private))

struct _{cc}Private
{{
    /* Private members */
}};

G_DEFINE_TYPE ({cc}, {lc}, G_TYPE_OBJECT)

static void
{lc}_finalize (GObject *object)
{{
\tG_OBJECT_CLASS ({lc}_parent_class)->finalize (object);
}}

static void
{lc}_class_init ({cc} *klass)
{{
\tGObjectClass *object_class = G_OBJECT_CLASS (klass);

\tobject_class->finalize = {lc}_finalize;

\tg_type_class_add_private (object_class, sizeof ({cc}Private));
}}

static void
{lc}_init ({cc} *self)
{{
\t {cc}Private *priv;
\t self->priv = priv = {uc}_GET_PRIVATE (self);
\t/* Initialize private members */
}}

/**
 * {lc}_new:
 *
 * Creates a new #{cc} object with default values.
 *
 * Returns: (transfer full): a new #{cc} object.
 */
{cc} *
{lc}_new (void)
{{
\treturn g_object_new ({uc_prefix}_TYPE_{uc_suffix}, NULL);
}}
"""

LICENSE_GPL = """\
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
