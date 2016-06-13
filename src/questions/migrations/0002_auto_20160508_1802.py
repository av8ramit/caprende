# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 18:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.CharField(choices=[(b'GRE: Verbal: Sentence Completion', b'GRE: Verbal: Sentence Completion'), (b'GRE: Verbal: Reading Comprehension', b'GRE: Verbal: Reading Comprehension'), (b'GRE: Math: Numbers and Operations', b'GRE: Math: Numbers and Operations'), (b'GRE: Math: Algebra and Functions', b'GRE: Math: Algebra and Functions'), (b'GRE: Math: Geometry and Measurement', b'GRE: Math: Geometry and Measurement'), (b'GRE: Math: Data Analysis, Statistics, and Probability Analytics', b'GRE: Math: Data Analysis, Statistics, and Probability Analytics')], default='a', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='subcategory',
            field=models.CharField(choices=[(b'GRE: Verbal: Sentence Completion: Context Single Word Replacement', b'GRE: Verbal: Sentence Completion: Context Single Word Replacement'), (b'GRE: Verbal: Sentence Completion: Inference Double Word Replacement', b'GRE: Verbal: Sentence Completion: Inference Double Word Replacement'), (b'GRE: Verbal: Sentence Completion: Synonymous Double Word Replacement', b'GRE: Verbal: Sentence Completion: Synonymous Double Word Replacement'), (b'GRE: Verbal: Reading Comprehension: Main Idea', b'GRE: Verbal: Reading Comprehension: Main Idea'), (b'GRE: Verbal: Reading Comprehension: Purpose/Rhetorical Strategy', b'GRE: Verbal: Reading Comprehension: Purpose/Rhetorical Strategy'), (b'GRE: Verbal: Reading Comprehension: Comparison', b'GRE: Verbal: Reading Comprehension: Comparison'), (b'GRE: Verbal: Reading Comprehension: Tone and Style', b'GRE: Verbal: Reading Comprehension: Tone and Style'), (b'GRE: Verbal: Reading Comprehension: Vocabulary in Context', b'GRE: Verbal: Reading Comprehension: Vocabulary in Context'), (b'GRE: Math: Numbers and Operations: Integers', b'GRE: Math: Numbers and Operations: Integers'), (b'GRE: Math: Numbers and Operations: Fractions', b'GRE: Math: Numbers and Operations: Fractions'), (b'GRE: Math: Numbers and Operations: Decimals', b'GRE: Math: Numbers and Operations: Decimals'), (b'GRE: Math: Numbers and Operations: Percents', b'GRE: Math: Numbers and Operations: Percents'), (b'GRE: Math: Numbers and Operations: Addition', b'GRE: Math: Numbers and Operations: Addition'), (b'GRE: Math: Numbers and Operations: Multiplication', b'GRE: Math: Numbers and Operations: Multiplication'), (b'GRE: Math: Numbers and Operations: Number Lines', b'GRE: Math: Numbers and Operations: Number Lines'), (b'GRE: Math: Numbers and Operations: Prime Numbers', b'GRE: Math: Numbers and Operations: Prime Numbers'), (b'GRE: Math: Numbers and Operations: Conversions', b'GRE: Math: Numbers and Operations: Conversions'), (b'GRE: Math: Numbers and Operations: Determining Quantities with Ratios', b'GRE: Math: Numbers and Operations: Determining Quantities with Ratios'), (b'GRE: Math: Numbers and Operations: Sequences', b'GRE: Math: Numbers and Operations: Sequences'), (b'GRE: Math: Numbers and Operations: Sets', b'GRE: Math: Numbers and Operations: Sets'), (b'GRE: Math: Numbers and Operations: Counting Problems', b'GRE: Math: Numbers and Operations: Counting Problems'), (b'GRE: Math: Algebra and Functions: Solving Basic Algebra Equations', b'GRE: Math: Algebra and Functions: Solving Basic Algebra Equations'), (b'GRE: Math: Algebra and Functions: Factoring', b'GRE: Math: Algebra and Functions: Factoring'), (b'GRE: Math: Algebra and Functions: Slope of a Line', b'GRE: Math: Algebra and Functions: Slope of a Line'), (b'GRE: Math: Algebra and Functions: Slope Formula', b'GRE: Math: Algebra and Functions: Slope Formula'), (b'GRE: Math: Algebra and Functions: X and Y Intercepts', b'GRE: Math: Algebra and Functions: X and Y Intercepts'), (b'GRE: Math: Algebra and Functions: Solving Quadratic Equations', b'GRE: Math: Algebra and Functions: Solving Quadratic Equations'), (b'GRE: Math: Algebra and Functions: Solving Absolute Value Equations', b'GRE: Math: Algebra and Functions: Solving Absolute Value Equations'), (b'GRE: Math: Algebra and Functions: Solving Inequalities', b'GRE: Math: Algebra and Functions: Solving Inequalities'), (b'GRE: Math: Algebra and Functions: Systems of Equations', b'GRE: Math: Algebra and Functions: Systems of Equations'), (b'GRE: Math: Algebra and Functions: Exponents', b'GRE: Math: Algebra and Functions: Exponents'), (b'GRE: Math: Algebra and Functions: Roots', b'GRE: Math: Algebra and Functions: Roots'), (b'GRE: Math: Algebra and Functions: Solving Absolute Value Equations', b'GRE: Math: Algebra and Functions: Solving Absolute Value Equations'), (b'GRE: Math: Algebra and Functions: Direct/Inverse Variation', b'GRE: Math: Algebra and Functions: Direct/Inverse Variation'), (b'GRE: Math: Algebra and Functions: Solving Word Problems', b'GRE: Math: Algebra and Functions: Solving Word Problems'), (b'GRE: Math: Algebra and Functions: Functions', b'GRE: Math: Algebra and Functions: Functions'), (b'GRE: Math: Geometry and Measurement: Points on Lines', b'GRE: Math: Geometry and Measurement: Points on Lines'), (b'GRE: Math: Geometry and Measurement: Lines and Angles', b'GRE: Math: Geometry and Measurement: Lines and Angles'), (b'GRE: Math: Geometry and Measurement: Angles from Parallel and Intersecting Lines', b'GRE: Math: Geometry and Measurement: Angles from Parallel and Intersecting Lines'), (b'GRE: Math: Geometry and Measurement: Interior Angles in Triangles and Other Polygons', b'GRE: Math: Geometry and Measurement: Interior Angles in Triangles and Other Polygons'), (b'GRE: Math: Geometry and Measurement: Types of Triangles based on Angles', b'GRE: Math: Geometry and Measurement: Types of Triangles based on Angles'), (b'GRE: Math: Geometry and Measurement: Types of Triangles based on Sides', b'GRE: Math: Geometry and Measurement: Types of Triangles based on Sides'), (b'GRE: Math: Geometry and Measurement: Special Triangle Rules', b'GRE: Math: Geometry and Measurement: Special Triangle Rules'), (b'GRE: Math: Geometry and Measurement: Perimeter and Area', b'GRE: Math: Geometry and Measurement: Perimeter and Area'), (b'GRE: Math: Geometry and Measurement: Volume', b'GRE: Math: Geometry and Measurement: Volume'), (b'GRE: Math: Geometry and Measurement: Arc Lengths and Areas for Sectors', b'GRE: Math: Geometry and Measurement: Arc Lengths and Areas for Sectors'), (b'GRE: Math: Geometry and Measurement: Midpoint Formula', b'GRE: Math: Geometry and Measurement: Midpoint Formula'), (b'GRE: Math: Geometry and Measurement: Distance Formula', b'GRE: Math: Geometry and Measurement: Distance Formula'), (b'GRE: Math: Geometry and Measurement: Polygon Properties', b'GRE: Math: Geometry and Measurement: Polygon Properties'), (b'GRE: Math: Geometry and Measurement: Logic', b'GRE: Math: Geometry and Measurement: Logic'), (b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Data Analysis', b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Data Analysis'), (b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Average', b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Average'), (b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Median', b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Median'), (b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Mode', b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Mode'), (b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Probability', b'GRE: Math: Data Analysis, Statistics, and Probability Analytics: Probability')], default='1', max_length=120),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='section',
            field=models.CharField(choices=[(b'GRE: Verbal', b'GRE: Verbal'), (b'GRE: Math', b'GRE: Math')], max_length=120),
        ),
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.CharField(choices=[(b'LSAT', b'LSAT'), (b'GRE', b'GRE')], max_length=120),
        ),
    ]