# Keep existing VPC resources (and the users table) in place after the move
# from hand-numbered resources to count-based ones.

moved {
  from = aws_subnet.public_1
  to   = aws_subnet.public[0]
}

moved {
  from = aws_subnet.public_2
  to   = aws_subnet.public[1]
}

moved {
  from = aws_subnet.private_1
  to   = aws_subnet.private[0]
}

moved {
  from = aws_subnet.private_2
  to   = aws_subnet.private[1]
}

moved {
  from = aws_eip.nat_1
  to   = aws_eip.nat[0]
}

moved {
  from = aws_nat_gateway.ngw_1
  to   = aws_nat_gateway.this[0]
}

moved {
  from = aws_route.public
  to   = aws_route.public_internet
}

moved {
  from = aws_route_table_association.public_1
  to   = aws_route_table_association.public[0]
}

moved {
  from = aws_route_table_association.public_2
  to   = aws_route_table_association.public[1]
}

moved {
  from = aws_route_table.private_1
  to   = aws_route_table.private[0]
}

moved {
  from = aws_route_table.private_2
  to   = aws_route_table.private[1]
}

moved {
  from = aws_route.private_1
  to   = aws_route.private_nat[0]
}

moved {
  from = aws_route.private_2
  to   = aws_route.private_nat[1]
}

moved {
  from = aws_route_table_association.private_1
  to   = aws_route_table_association.private[0]
}

moved {
  from = aws_route_table_association.private_2
  to   = aws_route_table_association.private[1]
}

moved {
  from = aws_vpc_endpoint.dynamodb_Endpoint
  to   = aws_vpc_endpoint.dynamodb
}
