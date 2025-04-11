class RoundedRectangle(pyglet.shapes.ShapeBase):

    def __init__(
            self,
            x: float, y: float,
            width: float, height: float,
            radius: _RadiusT | tuple[_RadiusT, _RadiusT, _RadiusT, _RadiusT],
            segments: int | tuple[int, int, int, int] | None = None,
            color: tuple[int, int, int, int] | tuple[int, int, int] = (255, 255, 255, 255),
            blend_src: int = GL_SRC_ALPHA,
            blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
            batch: Batch | None = None,
            group: Group | None = None,
            program: ShaderProgram | None = None,
    ) -> None:
        """Create a rectangle with rounded corners.

        The rectangle's anchor point defaults to the ``(x, y)``
        coordinates, which are at the bottom left.

        Args:
            x:
                The X coordinate of the rectangle.
            y:
                The Y coordinate of the rectangle.
            width:
                The width of the rectangle.
            height:
                The height of the rectangle.
            radius:
                One or four values to specify the radii used for the rounded corners.
                If one value is given, all corners will use the same value. If four values
                are given, it will specify the radii used for the rounded corners clockwise:
                bottom-left, top-left, top-right, bottom-right. A value can be either a single
                float, or a tuple of two floats to specify different x,y dimensions.
            segments:
                You can optionally specify how many distinct triangles each rounded corner
                should be made from. This can be one int for all corners, or a tuple of
                four ints for each corner, specified clockwise: bottom-left, top-left,
                top-right, bottom-right. If no value is specified, it will automatically
                calculated using the formula: ``max(14, int(radius / 1.25))``.
            color:
                The RGB or RGBA color of the rectangle, specified as a
                tuple of 3 or 4 ints in the range of 0-255. RGB colors
                will be treated as having an opacity of 255.
            blend_src:
                OpenGL blend source mode; for example, ``GL_SRC_ALPHA``.
            blend_dest:
                OpenGL blend destination mode; for example, ``GL_ONE_MINUS_SRC_ALPHA``.
            batch:
                Optional batch to add the shape to.
            group:
                Optional parent group of the shape.
            program:
                Optional shader program of the shape.
        """
        self._x = x
        self._y = y
        self._z = 0.0
        self._width = width
        self._height = height
        self._set_radius(radius)
        self._set_segments(segments)
        self._rotation = 0

        r, g, b, *a = color
        self._rgba = r, g, b, a[0] if a else 255

        super().__init__(
            (sum(self._segments) + 4) * 3,
            blend_src, blend_dest, batch, group, program,
        )

    def _set_radius(self, radius: _RadiusT | tuple[_RadiusT, _RadiusT, _RadiusT, _RadiusT]) -> None:
        if isinstance(radius, (int, float)):
            self._radius = ((radius, radius),) * 4
        elif len(radius) == 2:
            self._radius = (radius,) * 4
        else:
            assert len(radius) == 4
            self._radius = []
            for value in radius:
                if isinstance(value, (int, float)):
                    self._radius.append((value, value))
                else:
                    assert len(value) == 2
                    self._radius.append(value)

    def _set_segments(self, segments: int | tuple[int, int, int, int] | None) -> None:
        if segments is None:
            self._segments = tuple(int(max(a, b) / 1.25) for a, b in self._radius)
        elif isinstance(segments, int):
            self._segments = (segments,) * 4
        else:
            assert len(segments) == 4
            self._segments = segments

    def __contains__(self, point: tuple[float, float]) -> bool:
        assert len(point) == 2
        point = _rotate_point((self._x, self._y), point, math.radians(self._rotation))
        x, y = self._x - self._anchor_x, self._y - self._anchor_y
        return x < point[0] < x + self._width and y < point[1] < y + self._height

    def _create_vertex_list(self) -> None:
        self._vertex_list = self._program.vertex_list(
            self._num_verts, self._draw_mode, self._batch, self._group,
            position=('f', self._get_vertices()),
            color=('Bn', self._rgba * self._num_verts),
            translation=('f', (self._x, self._y) * self._num_verts))

    def _get_vertices(self) -> Sequence[float]:
        if not self._visible:
            return (0, 0) * self._num_verts

        x = -self._anchor_x
        y = -self._anchor_y

        points = []
        # arc_x, arc_y, start_angle
        arc_positions = [
            # bottom-left
            (x + self._radius[0][0],
             y + self._radius[0][1], math.pi * 3 / 2),
            # top-left
            (x + self._radius[1][0],
             y + self._height - self._radius[1][1], math.pi),
            # top-right
            (x + self._width - self._radius[2][0],
             y + self._height - self._radius[2][1], math.pi / 2),
            # bottom-right
            (x + self._width - self._radius[3][0],
             y + self._radius[3][1], 0),
        ]

        for (rx, ry), (arc_x, arc_y, arc_start), segments in zip(self._radius, arc_positions, self._segments):
            tau_segs = -math.pi / 2 / segments
            points.extend([(arc_x + rx * math.cos(i * tau_segs + arc_start),
                            arc_y + ry * math.sin(i * tau_segs + arc_start)) for i in range(segments + 1)])

        center_x = self._width / 2
        center_y = self._height / 2
        vertices = []
        for i, point in enumerate(points):
            triangle = center_x, center_y, *points[i - 1], *point
            vertices.extend(triangle)

        return vertices

    def _update_vertices(self) -> None:
        self._vertex_list.position[:] = self._get_vertices()

    @property
    def width(self) -> float:
        """Get/set width of the rectangle.

        The new left and right of the rectangle will be set relative to
        its :py:attr:`.anchor_x` value.
        """
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value
        self._update_vertices()

    @property
    def height(self) -> float:
        """Get/set the height of the rectangle.

        The bottom and top of the rectangle will be positioned relative
        to its :py:attr:`.anchor_y` value.
        """
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value
        self._update_vertices()

    @property
    def radius(self) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
        return self._radius

    @radius.setter
    def radius(self, value: _RadiusT | tuple[_RadiusT, _RadiusT, _RadiusT, _RadiusT]) -> None:
        self._set_radius(value)
        self._update_vertices()