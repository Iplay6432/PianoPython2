/*
 * [RoundPolygon.java]
 *
 * Summary: Computes, draws or fills rounded corners on polygons.
 *
 * Copyright: (c) 2011-2017 Roedy Green, Canadian Mind Products, http://mindprod.com
 *
 * Licence: This software may be copied and used freely for any purpose but military.
 *          http://mindprod.com/contact/nonmil.html
 *
 * Requires: JDK 1.8+
 *
 * Created with: JetBrains IntelliJ IDEA IDE http://www.jetbrains.com/idea/
 *
 * Version History:
 *  1.0 2011-01-09 initial version
 *  1.1 2011-01-10 improve artifacts using setOpaque, super.paintComponent and Graphics.create
 *  1.2 2011-01-19 drawRoundedPolygon fillRoundedPolygon
 */

import java.awt.Graphics;
import java.awt.Polygon;
import java.awt.geom.AffineTransform;
import java.awt.geom.NoninvertibleTransformException;
import java.awt.geom.Point2D;

/**
 * Computes, draws or fills rounded corners on polygons.
 *
 * @author Roedy Green, Canadian Mind Products
 * @version 1.2 2011-01-19 drawRoundPolygon fillRoundPolygon
 * @since 2011-01-09
 */
class RoundPolygon {
    /**
     * dummy constructor. All methods are static
     */
    private RoundPolygon() {
    }

    /**
     * two lines meet at a point. We provide the coordinates to draw a rounded
     * corner where they meet.
     * This is pure math. It is up to you draw. Not normally used except by
     * drawRoundPolygon and fillRoundPolygon.
     *
     * @param x1d    starting point x
     * @param y1d    starting point y
     * @param x3d    joining point x
     * @param y3d    jointing point y
     * @param x5d    end point x
     * @param y5d    end point y
     * @param radius radius of the arc used to round the corner.
     *
     * @return RoundedCorner object containing 9 results needed to draw the arc and
     *         lead in line segments.
     * @see #drawRoundPolygon
     * @see #fillRoundPolygon
     */
    public static RoundCornerCoordinates computeCoordinates(double x1d, double y1d, double x3d, double y3d,
            double x5d, double y5d, double radius) {
        // Math was done using trigonometry and analytical geometry.
        // Draw a diagram, label points, write down equations for relations between
        // sides.
        // Transform coordinates so that lines meet at x3d,y3d origin 0,0 and rotate so
        // that line from x1,y1d
        // x5d,y5d are at symmetrical about the x-axis
        // computeCoordinates how much rotation we need to position the two lines
        // symmetrically about the x axis.
        // still using original drawing coordinates.
        // upper angle at (3) relative to x axis
        double theta1 = Math.atan2(y3d - y1d, x1d - x3d); // convert to y is up
        // lower angle at (3) relative to x axis
        double theta5 = Math.atan2(y3d - y5d, x5d - x3d);
        // if theta1 == -theta5, there would be no rotation needed.
        // positive rotation is counterclockwise.
        double rot = -(theta5 + theta1) / 2;
        // transform needs to:
        // invert y axis so grows down.
        // move origin to x3d,y3d
        // rotate,
        // specified in reverse order
        final AffineTransform at = AffineTransform.getRotateInstance(rot);
        at.translate(-x3d, y3d);
        at.scale(1, -1);
        final AffineTransform undo;
        try {
            undo = at.createInverse();
        } catch (NoninvertibleTransformException e) {
            return null;
        }
        final Point2D x1y1toCart = new Point2D.Double(x1d, y1d);
        at.transform(x1y1toCart, x1y1toCart);
        final double x1c = x1y1toCart.getX();
        final double y1c = x1y1toCart.getY();
        // don't need x3c,y3c = 0,0 or x5c,y5c
        // Solve for x2, y2, xc
        final double h1c = Math.sqrt(x1c * x1c + y1c * y1c);
        // where first segment touches circle. not upper left corner of circle bounding
        // box
        double x2c = (radius * x1c * x1c) / (h1c * y1c); // derived from tan theta == y2/x2 == y1d/x1d
        double y2c = (radius * x1c) / h1c; // derived from cos theta == y2/r == x1d/h1c
        // where second segment touches circle
        double x4c = x2c;
        double y4c = -y2c;
        // computeCoordinates center of circle
        double root = Math.sqrt(radius * radius - y2c * y2c);
        // there are two solutions, we want the one further away from x3d=0
        double x6c = ((x2c + root) * (x2c + root) >= (x2c - root) * (x2c - root)) ? (x2c + root)
                : (x2c
                        -
                        root);
        double y6c = 0;
        // undo the transform, back to Java2D coordinates
        final Point2D x2y2ToDrawing = new Point2D.Double(x2c, y2c);
        undo.transform(x2y2ToDrawing, x2y2ToDrawing);
        final double x2d = x2y2ToDrawing.getX();
        final double y2d = x2y2ToDrawing.getY();
        final Point2D x4y4ToDrawing = new Point2D.Double(x4c, y4c);
        undo.transform(x4y4ToDrawing, x4y4ToDrawing);
        final double x4d = x4y4ToDrawing.getX();
        final double y4d = x4y4ToDrawing.getY();
        // center of circle
        final Point2D x6y6ToDrawing = new Point2D.Double(x6c, y6c);
        undo.transform(x6y6ToDrawing, x6y6ToDrawing);
        final double x6d = x6y6ToDrawing.getX();
        final double y6d = x6y6ToDrawing.getY();
        // computeCoordinates bounding box in Java2D coordinates with y growing down.
        double xbd = x6d - radius;
        double ybd = y6d - radius;
        double hbd = radius * 2;
        // angles here are in radians. result will be -pi .. +pi. Must do this is
        // drawing coordinates.
        double startAngle = Math.atan2(y6d - y2d, x2d - x6d); // flip sign
        if (startAngle < 0) {
            startAngle += Math.PI * 2;
        }
        double stopAngle = Math.atan2(y6d - y4d, x4d - x6d); // flip sign
        if (stopAngle < 0) {
            stopAngle += Math.PI * 2;
        }
        double arcAngle = stopAngle - startAngle;
        if (arcAngle < 0) {
            arcAngle += Math.PI * 2;
        }
        return new RoundCornerCoordinates(xbd, ybd, hbd, Math.toDegrees(startAngle), Math.toDegrees(arcAngle),
                x1d, y1d, x2d, y2d, x3d, y3d, x4d, y4d, x5d, y5d, x6d, y6d);
    }

    /**
     * Draw the outline of a polygon using rounded corners. Similar to
     * Graphics.drawRoundRect.
     * Does not yet word with concave angles
     *
     * @param g      graphics context
     * @param p      Polygon
     * @param radius radius of rounding arcs
     *
     * @see java.awt.Graphics#drawRoundRect(int, int, int, int, int, int)
     */
    public static void drawRoundPolygon(final Graphics g, final Polygon p, final int radius) {
        drawRoundPolygon(g, p.xpoints, p.ypoints, radius);
    }

    /**
     * Draw the outline of a polygon using rounded corners. Similar to
     * Graphics.drawRoundRect.
     * POints should be in counterclockwise order.
     *
     * @param g       graphics context
     * @param xPoints array of xPoints for the polygon points
     * @param yPoints array of yPoints for the polygon points
     * @param radius  radius of rounding arcs
     *
     * @see java.awt.Graphics#drawRoundRect(int, int, int, int, int, int)
     */
    public static void drawRoundPolygon(final Graphics g, final int[] xPoints, final int[] yPoints, final int radius) {
        assert xPoints.length >= 3 : "drawRoundPolygon requires at least three points.";
        assert xPoints.length == yPoints.length : "drawRoundPolygon must have an equal number of xPoints and yPoints.";
        // in drawing coordinates points are in counterclockwise order.
        // compute all points before doing any drawing.
        RoundCornerCoordinates[] corners = new RoundCornerCoordinates[xPoints.length];
        for (int corner = 0; corner < xPoints.length; corner++) {
            int prev = corner - 1;
            if (prev < 0) {
                prev += xPoints.length;
            }
            int next = corner + 1;
            if (next >= xPoints.length) {
                next -= xPoints.length;
            }
            int x1 = xPoints[prev];
            int y1 = yPoints[prev];
            int x3 = xPoints[corner];
            int y3 = yPoints[corner];
            int x5 = xPoints[next];
            int y5 = yPoints[next];
            corners[corner] = computeCoordinates(x1, y1, x3, y3, x5, y5, radius);
        }
        for (int corner = 0; corner < xPoints.length; corner++) {
            int prev = corner - 1;
            if (prev < 0) {
                prev += xPoints.length;
            }
            RoundCornerCoordinates c1 = corners[prev];
            RoundCornerCoordinates c3 = corners[corner];
            g.drawLine(c1.getX4(), c1.getY4(), c3.getX2(), c3.getY2());
            g.drawArc(c3.getXb(), c3.getYb(), c3.getHb(), c3.getHb(), c3.getStartAngle(), c3.getArcAngle());
            // draw the line 4 to 5 later when we do the next corner.
        }
    }

    /**
     * Fill a polygon using rounded corners. Similar to Graphics.fillRoundRect.
     *
     * @param g      graphics context
     * @param p      Polygon
     * @param radius radius of rounding arcs
     *
     * @see java.awt.Graphics#fillRoundRect(int, int, int, int, int, int)
     */
    public static void fillRoundPolygon(final Graphics g, final Polygon p, final int radius) {
        fillRoundPolygon(g, p.xpoints, p.ypoints, radius);
    }

    /**
     * Fill a polygon using rounded corners. Similar to Graphics.fillRoundRect.
     *
     * @param g       graphics context
     * @param xPoints array of xPoints for the polygon points
     * @param yPoints array of yPoints for the polygon points
     * @param radius  radius of rounding arcs
     *
     * @see java.awt.Graphics#fillRoundRect(int, int, int, int, int, int)
     */
    public static void fillRoundPolygon(final Graphics g, final int[] xPoints, final int[] yPoints, final int radius) {
        assert xPoints.length >= 3 : "drawRoundPolygon requires at least three points.";
        assert xPoints.length == yPoints.length : "drawRoundPolygon must have an equal number of xPoints and yPoints.";
        // in drawing coordinates points are in counter clockwise order.
        // compute all points before doing any drawing.
        RoundCornerCoordinates[] corners = new RoundCornerCoordinates[xPoints.length];
        for (int corner = 0; corner < corners.length; corner++) {
            int prev = corner - 1;
            if (prev < 0) {
                prev += xPoints.length;
            }
            int next = corner + 1;
            if (next >= xPoints.length) {
                next -= xPoints.length;
            }
            int x1 = xPoints[prev];
            int y1 = yPoints[prev];
            int x3 = xPoints[corner];
            int y3 = yPoints[corner];
            int x5 = xPoints[next];
            int y5 = yPoints[next];
            corners[corner] = computeCoordinates(x1, y1, x3, y3, x5, y5, radius);
        }
        final int[] xe = new int[corners.length * 2];
        final int[] ye = new int[corners.length * 2];
        int j = 0;
        for (int corner = 0; corner < xPoints.length; corner++) {
            // collect corners of inside polygon
            RoundCornerCoordinates aCorner = corners[corner];
            xe[j] = aCorner.getX2();
            ye[j] = aCorner.getY2();
            xe[j + 1] = aCorner.getX4();
            ye[j + 1] = aCorner.getY4();
            j += 2;
        }
        g.fillPolygon(xe, ye, xe.length);
        for (int corner = 0; corner < corners.length; corner++) {
            int prev = corner - 1;
            if (prev < 0) {
                prev += xPoints.length;
            }
            RoundCornerCoordinates c1 = corners[prev];
            RoundCornerCoordinates c3 = corners[corner];
            g.drawLine(c1.getX4(), c1.getY4(), c3.getX2(), c3.getY2());
            g.fillArc(c3.getXb(), c3.getYb(), c3.getHb(), c3.getHb(), c3.getStartAngle(), c3.getArcAngle());
            // draw the line 4 to 5 later when we do the next corner.
        }
    }

    /**
     * inner class to contain computational results for one corner.
     * Not normally used except by drawRoundPolygon and fillRoundPolygon.
     */
    public static class RoundCornerCoordinates {
        /**
         * size of the the arc in degrees not radians, Not the end arc angle.
         */
        final double arcAngle;

        /**
         * height (and width) of arc bounding box
         */
        final double hb;

        /**
         * where to start drawing the arc in degrees, not radians. 0 = 3 o'clock
         * counterclockwise.
         */
        final double startAngle;

        /**
         * start, Not really necessary since caller knows this already.
         */
        final double x1;

        /**
         * where first segment touches circle.
         */
        final double x2;

        /**
         * mid, Not really necessary since caller knows this already.
         */
        final double x3;

        /**
         * where second segment touches circle
         */
        final double x4;

        /**
         * end, Not really necessary since caller knows this already.
         */
        final double x5;

        /**
         * center of circle.
         */
        final double x6;

        /**
         * the center of the circle, not the upper left corner of the circle bounding
         * box
         */
        final double xb;

        /**
         * start. Not really necessary since caller knows this already.
         */
        final double y1;

        /**
         * where first segment touches circle.
         */
        final double y2;

        /**
         * mid. Not really necessary since caller knows this already.
         */
        final double y3;

        /**
         * where second segment touches circle
         */
        final double y4;

        /**
         * end. Not really necessary since caller knows this already.
         */
        final double y5;

        /**
         * center of circle
         */
        final double y6;

        /**
         * the center of the circle, not the upper left corner of the circle bounding
         * box
         */
        final double yb;

        /**
         * constructor to bundle the results of RoundedCorner.computeCoordinates
         *
         * @param xb         top left corner of arc bounding box
         * @param yb         top left corner of arc bounding box
         * @param hb         height of bounding box
         * @param startAngle angle in degrees counterclockwise to start drawing arc.
         * @param arcAngle   size of angle in degrees (end-start angle)
         * @param x1         start point
         * @param y1         start port
         * @param x2         where arc starts
         * @param y2         where arc starts
         * @param x3         mid point
         * @param y3         mid point
         * @param x4         where arc ends
         * @param y4         where arc ends
         * @param x5         end point
         * @param y5         end point
         * @param x6         center of circle
         * @param y6         center of circle
         */
        RoundCornerCoordinates(
                final double xb,
                final double yb,
                final double hb,
                final double startAngle,
                final double arcAngle,
                final double x1,
                final double y1,
                final double x2,
                final double y2,
                final double x3,
                final double y3,
                final double x4,
                final double y4,
                final double x5,
                final double y5,
                final double x6,
                final double y6) {
            this.xb = xb;
            this.yb = yb;
            this.hb = hb;
            this.startAngle = startAngle;
            this.arcAngle = arcAngle;
            this.x1 = x1;
            this.y1 = y1;
            this.x2 = x2;
            this.y2 = y2;
            this.x3 = x3;
            this.y3 = y3;
            this.x4 = x4;
            this.y4 = y4;
            this.x5 = x5;
            this.y5 = y5;
            this.x6 = x6;
            this.y6 = y6;
        }

        /**
         * size of the the arc in degrees not radians, Not the end arc angle, measured
         * counterclockwise.
         *
         * @return and in degrees
         */
        public int getArcAngle() {
            return (int) Math.floor(arcAngle + .5);
        }

        /**
         * height (and width) of arc bounding box
         *
         * @return height of box in pixels
         */
        public int getHb() {
            return (int) Math.floor(hb + .5);
        }

        /**
         * where to start drawing the arc in degrees, not radians. 0 = 3 o'clock
         * counterclockwise.
         *
         * @return angle in degrees
         */
        public int getStartAngle() {
            return (int) Math.floor(startAngle + .5);
        }

        /**
         * start point.
         *
         * @return x in drawing coordinates
         */
        public int getX1() {
            return (int) Math.floor(x1 + .5);
        }

        /**
         * where first segment touches circle.
         *
         * @return x in drawing coordinates
         */
        public int getX2() {
            return (int) Math.floor(x2 + .5);
        }

        /**
         * mid point.
         *
         * @return x in drawing coordinates
         */
        public int getX3() {
            return (int) Math.floor(x3 + .5);
        }

        /**
         * where second segment touches circle
         *
         * @return x in drawing coordinates
         */
        public int getX4() {
            return (int) Math.floor(x4 + .5);
        }

        /**
         * end point.
         *
         * @return x in drawing coordinates.
         */
        public int getX5() {
            return (int) Math.floor(x5 + .5);
        }

        /**
         * center of circle.
         *
         * @return x in drawing coordinates
         */
        public int getX6() {
            return (int) Math.floor(x6 + .5);
        }

        /**
         * The upper left corner of the circle bounding box, not the center of the
         * circle,
         *
         * @return x in drawing coordinates
         */
        public int getXb() {
            return (int) Math.floor(xb + .5);
        }

        /**
         * where start.
         *
         * @return y in drawing coordinates
         */
        public int getY1() {
            return (int) Math.floor(y1 + .5);
        }

        /**
         * where first segment touches circle.
         *
         * @return y in drawing coordinates
         */
        public int getY2() {
            return (int) Math.floor(y2 + .5);
        }

        /**
         * where mid point
         *
         * @return y in drawing coordinates
         */
        public int getY3() {
            return (int) Math.floor(y3 + .5);
        }

        /**
         * where second segment touches circle
         *
         * @return y in drawing coordinates
         */
        public int getY4() {
            return (int) Math.floor(y4 + .5);
        }

        /**
         * end point
         *
         * @return y in drawing coordinates
         */
        public int getY5() {
            return (int) Math.floor(y5 + .5);
        }

        /**
         * center of circle
         *
         * @return y in drawing coordinates
         */
        public int getY6() {
            return (int) Math.floor(y6 + .5);
        }

        /**
         * the upper left corner of the circle bounding box, not the center
         *
         * @return y in drawing coordinates
         */
        public int getYb() {
            return (int) Math.floor(yb + .5);
        }

        /**
         * debugging tool
         */
        public String toString() {
            return "drawing: xb,yb:("
                    + xb
                    + ","
                    + yb
                    + ") hb:"
                    + hb
                    + " startAngle:"
                    + startAngle
                    + " arcAngle:"
                    + arcAngle
                    + " start x1,y1:("
                    + x1
                    + ","
                    + y1
                    + ") start arc x2,y2:("
                    + x2
                    + ","
                    + y2
                    + ") mid x3,y3:("
                    + x3
                    + ","
                    + y3
                    + ") end arc x4,y4:("
                    + x4
                    + ","
                    + y4
                    + ") end x5,y5:("
                    + x5
                    + ","
                    + y5
                    + ") circle center x6,y6:("
                    + x6
                    + ","
                    + y6
                    + ")";
        }
    }
}
